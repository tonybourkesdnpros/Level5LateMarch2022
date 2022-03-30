from cvplibrary import CVPGlobalVariables, GlobalVariableNames
import yaml
import ssl
from cvplibrary import RestClient

def get_hostname():

  labels = CVPGlobalVariables.getValue(GlobalVariableNames.CVP_SYSTEM_LABELS)
  
  
  for item in labels:
    key, value = item.split(':')
    if key == 'hostname':
      hostname = value
      
  return hostname

hostname = get_hostname()

if 'DC1' in hostname:
  DC = 'DC1'
if 'DC2' in hostname:
  DC = 'DC2'

ssl._create_default_https_context = ssl._create_unverified_context
configlet = 'underlay_yaml'
cvp_url = 'https://192.168.0.5/cvpservice/'
client = RestClient(cvp_url+'configlet/getConfigletByName.do?name='+configlet,'GET')
if client.connect():
  raw = yaml.safe_load(client.getResponse())
underlay = yaml.safe_load(raw['config'])


route_maps = """
ip prefix-list LOOPBACK
    seq 10 permit 192.168.101.0/24 eq 32
    seq 20 permit 192.168.102.0/24 eq 32
    seq 30 permit 192.168.201.0/24 eq 32
    seq 40 permit 192.168.202.0/24 eq 32
    seq 50 permit 192.168.253.0/24 eq 32

route-map LOOPBACK permit 10
   match ip address prefix-list LOOPBACK

peer-filter LEAF-AS-RANGE
   10 match as-range 65000-65535 result accept
"""

def gen_interfaces():
  for iface in underlay[hostname]['interfaces']:
    ip = str(underlay[hostname]['interfaces'][iface]['ipv4'])
    mask = str(underlay[hostname]['interfaces'][iface]['mask'])
    print("interface %s") % iface
    print("  ip address %s/%s") % (ip, mask)
    if 'Ethernet' in iface:
      print("  no switchport")
      print("  mtu 9214")
    

def gen_leaf_BGP():
  print(route_maps)
  BGP_ASN = underlay[hostname]['BGP']['ASN']
  router_ID = underlay[hostname]['interfaces']['loopback0']['ipv4'] 
  print("router bgp %s") % BGP_ASN
  print("  router-id %s") % router_ID
  print("  no bgp default ipv4-unicast")
  print("  maximum-paths 3")
  print("  distance bgp 20 200 200")
  print("  neighbor Underlay peer group") 
  spine_ASN = underlay['global'][DC]['spine_ASN']
  print("  neighbor Underlay remote-as %s") % spine_ASN

  print("  neighbor Underlay send-community")
  print("  neighbor Underlay maximum-routes 12000")
  print("  redistribute connected route-map LOOPBACK")
  for spine_underlay_peer in underlay[hostname]['BGP']['spine-peers']:
    print("  neighbor %s peer group Underlay") % spine_underlay_peer
   
   
  print("  neighbor EVPN peer group")
  print("  neighbor EVPN remote-as %s") % spine_ASN

  print("  neighbor EVPN update-source Loopback0")
  print("  neighbor EVPN ebgp-multihop 3")
  print("  neighbor EVPN send-community extended")
  print("  neighbor EVPN maximum-routes 0")
  
  for spine_EVPN in underlay['global'][DC]['spine_peers']:
    print("  neighbor %s peer group EVPN") % spine_EVPN

  if 'border' in hostname:
    print("  neighbor EVPN_DCI peer group")
    print("  neighbor EVPN_DCI remote-as 65000")
    print("  neighbor EVPN_DCI update-source Loopback0")
    print("  neighbor EVPN_DCI ebgp-multihop 3")
    print("  neighbor EVPN_DCI send-community extended")
    print("  neighbor EVPN_DCI maximum-routes 0")
    print("  neighbor 192.168.253.1 peer group EVPN_DCI")


  if 'border' in hostname:
    print("  neighbor DCI peer group")
    print("  neighbor DCI remote-as 65000")
    print("  neighbor DCI send-community")
    print("  neighbor DCI maximum-routes 12000")
    for DCI_peer in underlay[hostname]['BGP']['DCI-peers']:
       print("  neighbor %s peer group DCI") % DCI_peer
    print("  address-family ipv4")
    print("     neighbor DCI activate")
    print("  address-family evpn")
    print("     neighbor EVPN_DCI activate")
    # neighbor LEAF_Peer activate   
    
      

  print("  address-family ipv4")
  print("     neighbor Underlay activate")
  print("  address-family evpn")
  print("     neighbor EVPN activate")

def gen_spine_BGP():
  print(route_maps)
  BGP_ASN = underlay[hostname]['BGP']['ASN']
  router_ID = underlay[hostname]['interfaces']['loopback0']['ipv4'] 
  print("router bgp %s") % BGP_ASN
  print("  router-id %s") % router_ID
  print("  no bgp default ipv4-unicast")
  print("  maximum-paths 3")
  print("  distance bgp 20 200 200")

  
  listen_range = underlay['global'][DC]['p2p']
  print("  bgp listen range %s peer-group LEAF_Underlay peer-filter LEAF-AS-RANGE") % listen_range

  print("  neighbor LEAF_Underlay peer group")
  print("  neighbor LEAF_Underlay send-community")
  print("  neighbor LEAF_Underlay maximum-routes 12000")

  EVPN_listen_range = underlay['global'][DC]['lo0']
  print("  neighbor EVPN peer group")
  print("  bgp listen range %s peer-group EVPN peer-filter LEAF-AS-RANGE") % EVPN_listen_range
  
    
  print("  neighbor EVPN update-source Loopback0")
  print("  neighbor EVPN ebgp-multihop 3")
  print("  neighbor EVPN send-community")
  print("  neighbor EVPN maximum-routes 0")

  print("  redistribute connected route-map LOOPBACK")
   
  # address-family evpn
  #   neighbor EVPN activate
  print("  address-family ipv4")
  print("    neighbor LEAF_Underlay activate")
  print("  address-family evpn")
  print("    neighbor EVPN activate")

  
  
  


gen_interfaces()

if 'leaf' in hostname:
  gen_leaf_BGP()
if 'spine' in hostname:
  gen_spine_BGP()