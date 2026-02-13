import ifcopenshell
import ifcopenshell.util.selector
from collections import defaultdict

def main():

    while True:

        try:
            input_file = input("Please enter IFC file path or type exit to quit: ")
            if input_file == "exit":
                break
            model = ifcopenshell.open(input_file)
            break
        except:
            print("Not a valid IFC file path.")
            pass

    while True:

        try:
            pset = input("Please enter Pset name (example: Pset_WallCommon) or type exit to quit: ")
            if pset == "exit":
                break
            if check_pset_exists(model, pset) == False:
                raise Exception
            break
        except:
            print("Pset not found.")
            pass
    
    while True:

        try:
            property = input("Please enter property name (example: FireRating) or type exit to quit: ")
            if property == "exit":
                break
            elements = ifcopenshell.util.selector.filter_elements(model, f"IfcElement, {pset}.{property} != NULL")
            if not elements:
                raise Exception
            break
        except:
            print("No elements with the requested property found in the Pset.")
            pass

    
    elements_with_properties = [Element(element, ifcopenshell.util.element.get_pset(element, pset, property)) for element in elements]
    
    grouped = defaultdict(list)

    for e in elements_with_properties:
        grouped[e.property].append(e)

    for property, group in grouped.items():
        print(property, [e.element for e in group])


    """for group in groups:

        r = 
        g = 
        b = 
        
        style = ifcopenshell.api.style.add_style(model)

        ifcopenshell.api.style.add_surface_style(model,
            style=style, ifc_class="IfcSurfaceStyleShading", attributes={
                "SurfaceColour": { "Name": 'RGB' + r + g + b, "Red": 1.0, "Green": 0.8, "Blue": 0.8 },
                "Transparency": 0.,
            })"""
            
            


def check_pset_exists(ifc_file, pset_name):
    
    property_sets = ifc_file.by_type("IfcPropertySet")

    for pset in property_sets:
        if pset.Name == pset_name:
            return True

    return False

class Element:
    def __init__(self, element, property):
        self.element = element
        self.property = property


if __name__ == "__main__":
    main()




