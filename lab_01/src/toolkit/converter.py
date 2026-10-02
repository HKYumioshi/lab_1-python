from toolkit.errors import ConverterError

def convert(value, quantity_from, quantity_to):
    allowed_quantities = ['mm', 'cm', 'm', 'km', 'g', 'kg', 'c', 'f', 'k']

    if quantity_from not in allowed_quantities:
        raise ConverterError(f"Unknown quantity {quantity_from}")

    if quantity_to not in allowed_quantities:
            raise ConverterError(f"Unknown quantity {quantity_to}")
    
    quantities = {
        "length": {
            "mm": 1,
            "cm": 10,
            "m": 1000,
            "km": 1000000
        },
        "weight": {
            "g": 1,
            "kg": 1000
        }
    }
    quantity_from, quantity_to = quantity_from.lower(), quantity_to.lower()

    length_or_weight = None

    for key in quantities:
        el = quantities[key]
        if ((quantity_from in el) and (quantity_to not in el)) or ((quantity_from not in el) and (quantity_to in el)):
            raise ConverterError("Can't convert value from one quantity to another")
        
        elif quantity_from in el and quantity_to in el:
            length_or_weight = 'length' if key == 'length' else 'weight'

    if length_or_weight:
        value = value * (quantities[length_or_weight][quantity_from] / quantities[length_or_weight][quantity_to]) 

    else:
        match quantity_from:
            case "c":
                if value < -273.15:
                    raise ConverterError("Temperature can't be below absolute zero")
                match quantity_to:
                    case "f":
                        value = value * 1.8 + 32
                    case "k":
                        value += 273.15
                    case "c":
                        pass
            case "k":
                if value < 0:
                    raise ConverterError("Temperature can't be below absolute zero")
                match quantity_to:
                    case "f":
                        value = (value - 273.15) * 1.8 + 32 
                    case "k":
                        pass
                    case "c":
                        value = value - 273.15
            case "f":
                if value < -459.67:
                    raise ConverterError("Temperature can't be below absolute zero")
                match quantity_to:
                    case "f":
                        pass
                    case "k":
                        value = (value - 32) * 5/9 + 273.15
                    case "c":
                       value = (value - 32) * 5/9

    return float(value)
