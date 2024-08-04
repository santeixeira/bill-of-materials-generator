import csv
import sys
import kicad_netlist_reader
import json

net = kicad_netlist_reader.netlist(sys.argv[1])

try:
    f = open(sys.argv[2], 'w')
except IOError:
    e = "Can't open output file for writing: " + sys.argv[2]
    print(__file__, ":", e, sys.stderr)
    f = sys.stdout

out = csv.writer(f, lineterminator='\n', delimiter=',', quotechar='\"', quoting=csv.QUOTE_ALL)

grand_total_cost = 0.0
total_items = 0
uniq_items = 0

out.writerow(['#',
    'Reference',
    'Value',
    'Footprint',
    'Qty',
    'Tolerance',	
    'Voltage',	
    'Wattage',	
    'Current',	
    'Frequency',	
    'Dielectric',	
    'Datasheet',	
    'Cost @ 10000',
    'Total Gross'
])

def total_cost(unit_cost, quantity):
    if not unit_cost:
        return 0
    return float(unit_cost)*int(quantity)

grouped = net.groupComponents()


for group in grouped:
    refs = ""

    for component in group:
        refs += component.getRef() + ", "
        c = component
        
    cost = c.getField("Cost @ 10000").replace('$', '')
        
    grand_total_cost += total_cost(cost, len(group))
    uniq_items += 1
    
    out.writerow([
        uniq_items,
        refs,
        c.getValue(),
        c.getField("Footprint"),
        len(group),
        c.getField("Tolerance"),
        c.getField("Voltage"),
        c.getField("Wattage"),
        c.getField("Current"),
        c.getField("Frequency"),
        c.getField("Dielectric"),
        c.getDatasheet(),
        c.getField("Cost @ 10000"),
        "${:.4f}".format(total_cost(cost, len(group)))
    ])
    
data = {}
data['bom'] = []
data['bom'].append({
    'total':  "${:.4f}".format(grand_total_cost),
    'uniq_items': uniq_items,
    'total_items': total_items
})

with open('./bom/data.json', 'w') as outfile:
    json.dump(data, outfile, indent=2)