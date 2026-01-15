import json


def get_membership(value, points):

    if not points:
        return 0.0
    
    sorted_points = sorted(points, key=lambda p: p[0])
    
    for i in range(len(sorted_points) - 1):
        x1, y1 = sorted_points[i]
        x2, y2 = sorted_points[i+1]
        
        if x1 <= value <= x2:
            if x1 == x2:
                return max(y1, y2)
            return y1 + (value - x1) * (y2 - y1) / (x2 - x1)
            
    return 0.0


def main(temp_json_str, control_json_str, rules_json_str, current_temp):
 
    try:
        temp_data = json.loads(temp_json_str)
        control_data = json.loads(control_json_str)
        
        rules_json_fixed = rules_json_str.replace("'", '"')
        try:
            rules_data = json.loads(rules_json_fixed)
        except json.JSONDecodeError:
            import ast
            rules_data = ast.literal_eval(rules_json_str)
    except (json.JSONDecodeError, ValueError, SyntaxError):
        return 0.0

    temp_terms = {item['id']: item['points'] for item in temp_data.get('температура', [])}
    control_terms = {item['id']: item['points'] for item in control_data.get('температура', [])}

    id_mapping = {
        "нормально": "комфортно",
        "холодно": "холодно",
        "жарко": "жарко",
        "интенсивно": "интенсивный",
        "умеренно": "умеренный",
        "слабо": "слабый"
    }

    min_s = 0.0
    max_s = 30.0 
    step = 0.1  
    
    steps_count = int((max_s - min_s) / step)
    s_values = [min_s + i * step for i in range(steps_count)]
    aggregated_membership = [0.0] * steps_count

    rule_fired = False
    
    for rule in rules_data:
        if len(rule) != 2:
            continue
            
        input_id_raw, output_id_raw = rule
        
        input_id = id_mapping.get(input_id_raw, input_id_raw)
        output_id = id_mapping.get(output_id_raw, output_id_raw)
        
        if input_id not in temp_terms or output_id not in control_terms:
            continue

        alpha = get_membership(current_temp, temp_terms[input_id])
        
        if alpha > 0:
            rule_fired = True
            
            output_points = control_terms[output_id]
            
            for i, s in enumerate(s_values):
                mu_term = get_membership(s, output_points)
                mu_implication = min(alpha, mu_term) # Clipping
                
                if mu_implication > aggregated_membership[i]:
                    aggregated_membership[i] = mu_implication

    if not rule_fired:
        return 0.0

    global_max = max(aggregated_membership)
    
  
    if global_max == 0:
        return 0.0
        
    for i, mu in enumerate(aggregated_membership):
        if abs(mu - global_max) < 1e-9:
            return s_values[i]

    return 0.0
