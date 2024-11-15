import pandas as pd
import re
from tqdm import tqdm
import os

# cross-platform 'downloads' directory 
downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")    

def replace_patterns(text, pattern_counters):
    patterns = [
        (r"{}, {}", "{},{}"),
        (r"{}x{}", "{} x {}"),
        (r"{}χ{}", "{} x {}"),
        (r"{} X {}", "{} x {}"),
        (r"{} Χ {}", "{} x {}"),
        (r"{} σε {}", "{}σε{} "),
        (r"{}-σε-{}", "{}σε{} "),
        (r"{}ΣΕ{}", "{}σε{} "),
        (r"{}Σε{}", "{}σε{} "),
        (r"{}in{}", "{}σε{} "),
        (r"{} in {}", "{}σε{} "),
        (r"{}-in-{}", "{}σε{} "),
        (r"{},{}", "{}.{}"),               
        (r"{}x\b", "{} x "),
        (r"{}χ\b", "{} x "),
        (r"{} x\b", "{} x "),  
        (r"{} χ\b", "{} x "),
        (r"^x{}", " x {}"),
        (r"^χ{}", " x {}"),
        (r"^x {}", " x {}"),  
        (r"^χ {}", " x {}"),
        # (r"(^|\s)x{}", " x {}"),
        # (r"(^|\s)χ{}", " x {}"),
        (r"{} γραμμάρια\b", "{} g "),
        (r"{} γραμμαρια\b", "{} g "),
        (r"{} γρ\.", "{} g "),
        (r"{} γρ\b", "{} g "),
        (r"{} γ\.", "{} g "),
        (r"{}γρ\.", "{} g "),
        (r"{}γρ\b", "{} g "),
        (r"{}γ\.", "{} g "),
        (r"{} grams\b", "{} g "),
        (r"{} gr\.", "{} g "),
        (r"{} gr\b", "{} g "),
        (r"{} g\.", "{} g "),
        (r"{} G\b", "{} g "),
        (r"{}gr\.", "{} g "),
        (r"{}gr\b", "{} g "),
        (r"{}Gr\b", "{} g "),
        (r"{}g\.", "{} g "),
        (r"{}g\b", "{} g "),
        (r"{}G\b", "{} g "),
        (r"{}G\.", "{} g "),          
        (r"{}ml\.", "{} ml "),
        (r"{}ml", "{} ml "),
        (r"{} ml\.", "{} ml "),
        (r"{} Ml\b", "{} ml "),
        (r"{} ML\b", "{} ml "),
        (r"{}Ml\b", "{} ml "),
        (r"{}ML", "{} ml "),
        (r"{}ug\.", "{} ug "),
        (r"{}ug", "{} ug "),
        (r"{} ug\.", "{} ug "),
        (r"{} Ug\b", "{} ug "),
        (r"{} UG\b", "{} ug "),
        (r"{}Ug\b", "{} ug "),
        (r"{}UG", "{} ug "),
        (r"{}μg\.", "{} ug "),
        (r"{}μg", "{} ug "),
        (r"{} μg\.", "{} ug "),
        (r"{} μg\b", "{} ug "),
        (r"{} μG\b", "{} ug "),
        (r"{}μg\b", "{} ug "),
        (r"{}μG", "{} ug "),                
        (r"{}mg\.", "{} mg "),
        (r"{}mg", "{} mg "),
        (r"{} mg\.", "{} mg "),          
        (r"{} Mg\b", "{} mg "),
        (r"{} MG\b", "{} mg "),
        (r"{}Mg\b", "{} mg "),
        (r"{}MG", "{} mg "),               
        (r"{}kg\.", "{} kg "),
        (r"{}kg", "{} kg "),
        (r"{}κγ\.", "{} kg "),
        (r"{}κγ", "{} kg "),
        (r"{} κγ\.", "{} kg "),
        (r"{} κγ", "{} kg "),                
        (r"{} κιλά\.", "{} kg "),
        (r"{} κιλα\b", "{} kg "),
        (r"{} kg\.", "{} kg "), 
        (r"{} Kg\b", "{} kg "),
        (r"{} KG\b", "{} kg "),
        (r"{}Kg\b", "{} kg "),
        (r"{}KG", "{} kg "),
        (r"{}kgr\.", "{} kg "),
        (r"{}kgr", "{} kg "),
        (r"{} kgr\.", "{} kg "),
        (r"{} kgr\b", "{} kg "),
        (r"{} Kgr\b", "{} kg "),
        (r"{} KGR\b", "{} kg "),
        (r"{}Kgr\b", "{} kg "),
        (r"{}KGR", "{} kg "),
        (r"{}0.05 l", "{}50 ml "),        
        (r"{} λτρ\.", "{} l "),   
        (r"{} λτρ\b", "{} l "),
        (r"{} λτ\.", "{} l "),
        (r"{} λτ\b", "{} l "),
        (r"{} λ\.", "{} l "),
        (r"{}λτ\.", "{} l "),
        (r"{}λτ", "{} l "),
        (r"{}λ\.", "{} l "),
        (r"{}ltr\.", "{} l "),
        (r"{}ltr\b", "{} l "),
        (r"{}lt\.", "{} l "),
        (r"{}lt", "{} l "),
        (r"{} lt\.", "{} l "),
        (r"{} lt\b", "{} l "),
        (r"{} λίτρα\b", "{} l "),
        (r"{} λιτρα\b", "{} l "),
        (r"{} l\.", "{} l "),
        (r"{} L\b", "{} l "),
        (r"{}l\.", "{} l "),
        (r"{}l\b", "{} l "),
        (r"{}L\.", "{} l "),
        (r"{}L\b", "{} l "),        
        (r"{}τεμαχιων\.", "{} τμχ "),
        (r"{}τεμαχιων\b", "{} τμχ "),
        (r"{} τεμαχιων\.", "{} τμχ "),
        (r"{} τεμαχιων\b", "{} τμχ "),
        (r"{}τεμάχια\.", "{} τμχ "),
        (r"{}τεμαχια\.", "{} τμχ "),
        (r"{}τεμάχια\b", "{} τμχ "),
        (r"{}τεμαχια\b", "{} τμχ "),
        (r"{}τεμάχιο\.", "{} τμχ "),
        (r"{}τεμαχιο\.", "{} τμχ "),
        (r"{}τεμάχιο\b", "{} τμχ "),
        (r"{}τεμαχιο\b", "{} τμχ "),
        (r"{} τεμάχια\.", "{} τμχ "),
        (r"{} τεμαχια\.", "{} τμχ "),
        (r"{} τεμάχια\b", "{} τμχ "),
        (r"{} τεμαχια\b", "{} τμχ "),        
        (r"{} τεμάχιο\.", "{} τμχ "),
        (r"{} τεμαχιο\.", "{} τμχ "),
        (r"{} τεμάχιο\b", "{} τμχ "),
        (r"{} τεμαχιο\b", "{} τμχ "),
        (r"{}Τεμάχ\.", "{} τμχ "),
        (r"{} Τεμάχ\.", "{} τμχ "),
        (r"{}Τεμαχ\b", "{} τμχ "),
        (r"{} Τεμαχ\b", "{} τμχ "),
        (r"{}Τεμά\.", "{} τμχ "),
        (r"{} Τεμά\.", "{} τμχ "),
        (r"{}Τεμα\b", "{} τμχ "),
        (r"{} Τεμα\b", "{} τμχ "),        
        (r"{}τμχ\.", "{} τμχ "),
        (r"{} τμχ\.", "{} τμχ "),
        (r"{}τμχ\b", "{} τμχ "),
        (r"{} τμχ\b", "{} τμχ "),
        (r"{}tmx\.", "{} τμχ "),
        (r"{} tmx\.", "{} τμχ "),
        (r"{}tmx\b", "{} τμχ "),
        (r"{} tmx\b", "{} τμχ "),        
        (r"{}τεμ\.", "{} τμχ "),
        (r"{} τεμ\.", "{} τμχ "), 
        (r"{}τεμ\b", "{} τμχ "),
        (r"{} τεμ\b", "{} τμχ "),
        # (r"{}t\.", "{} τμχ "),
        (r"{}τ\.", "{} τμχ "),
        # (r"{}t\b", "{} τμχ "),
        (r"{}τ\b", "{} τμχ "),
        # (r"{} t\.", "{} τμχ "),
        (r"{} τ\.", "{} τμχ "),
        # (r"{} t\b", "{} τμχ "),
        (r"{} τ\b", "{} τμχ "),                
        (r"{}pcs\.", "{} τμχ "),
        (r"{} pcs\.", "{} τμχ "),
        (r"{}pcs\b", "{} τμχ "),
        (r"{} pcs\b", "{} τμχ "),
        (r"{}pces\.", "{} τμχ "),
        (r"{} pces\.", "{} τμχ "),
        (r"{}pces\b", "{} τμχ "),
        (r"{} pces\b", "{} τμχ "),
        (r"{}pieces\.", "{} τμχ "),
        (r"{} pieces\.", "{} τμχ "),
        (r"{}pieces\b", "{} τμχ "),
        (r"{} pieces\b", "{} τμχ "),        
        (r"{} δώρο\.", "{} Δώρο "),
        (r"{}δώρο\.", "{} Δώρο "),
        (r"{} δώρο\b", "{} Δώρο "),
        (r"{}δώρο\b", "{} Δώρο "),
        (r"{} δώρ\.", "{} Δώρο "),
        (r"{}δώρ\.", "{} Δώρο "),
        (r"{} δώρ\b", "{} Δώρο "),
        (r"{}δώρ\b", "{} Δώρο "),
        (r"{}\s*ε\.", "{}€ "),
        (r"{}\s*e\.", "{}€ "),
        (r"{}\s*ε\b", "{}€ "),
        (r"{}\s*e\b", "{}€ "),
        (r"{}\s*ευρω\b", "{}€ "),
        (r"{}\s*euro\b", "{}€ "),
        (r"{}\s*φθηνότερα\b", "{}€ "),
        (r"{}\s*φθηνοτερα\b", "{}€ "),                           
#        (r"-\d{1,2},\d{1,2}", "{}€ "),
        (r"bottle", " μπουκάλι"),
        (r"btl\b", " μπουκάλι"),
        (r"μπουκ\b", " μπουκάλι"),
        (r"μπουκ\.", " μπουκάλι"),       
        (r"{}Μεζούρες", "{} Μεζούρες "),
        (r"{} Μεζ\.", "{} Μεζούρες "),
        (r"{}Μεζ\.", "{} Μεζούρες "),
        (r"{} Μεζ\b", "{} Μεζούρες "),
        (r"{}Μεζ\b", "{} Μεζούρες "),
        (r"{} Με\.", "{} Μεζούρες "),
        (r"{}Με\.", "{} Μεζούρες "),
        (r"{} Με\b", "{} Μεζούρες "),
        (r"{}Με\b", "{} Μεζούρες "),
        (r"{} tabs\.", "{} tabs "),
        (r"{}tabs\.", "{} tabs "),
        (r"{} tabs\b", "{} tabs "),
        (r"{}tabs\b", "{} tabs "),
        (r"{} tablets\.", "{} tabs "),
        (r"{}tablets\.", "{} tabs "),
        (r"{} tablets\b", "{} tabs "),
        (r"{}tablets\b", "{} tabs "),
        (r"{} ταμπλέτες\.", "{} tabs "),
        (r"{}ταμπλέτες\.", "{} tabs "),
        (r"{} ταμπλέτες\b", "{} tabs "),
        (r"{}ταμπλέτες\b", "{} tabs "),
        (r"{} ΤΑΜΠΛΕΤΕΣ\.", "{} tabs "),
        (r"{}ΤΑΜΠΛΕΤΕΣ\.", "{} tabs "),
        (r"{} ΤΑΜΠΛΕΤΕΣ\b", "{} tabs "),
        (r"{}ΤΑΜΠΛΕΤΕΣ\b", "{} tabs "),                  
        (r"{} κάψουλες\.", "{} caps "),
        (r"{}κάψουλες\.", "{} caps "),
        (r"{} κάψουλες\b", "{} caps "),
        (r"{}κάψουλες\b", "{} caps "),
        (r"{} ΚΑΨΟΥΛΕΣ\.", "{} caps "),
        (r"{}ΚΑΨΟΥΛΕΣ\.", "{} caps "),
        (r"{} ΚΑΨΟΥΛΕΣ\b", "{} caps "),
        (r"{}ΚΑΨΟΥΛΕΣ\b", "{} caps "),
        (r"{} caps\.", "{} caps "),
        (r"{}caps\.", "{} caps "),
        (r"{} caps\b", "{} caps "),
        (r"{}caps\b", "{} caps "),
        (r"{} capsules\.", "{} caps "),
        (r"{}capsules\.", "{} caps "),
        (r"{} capsules\b", "{} caps "),
        (r"{}capsules\b", "{} caps "),
        (r"{} δισκία\.", "{} δισκία "),
        (r"{}δισκία\.", "{} δισκία "),
        (r"{} δισκία\b", "{} δισκία "),
        (r"{}δισκία\b", "{} δισκία "),
        (r"{} ΔΙΣΚΙΑ\.", "{} δισκία "),
        (r"{}ΔΙΣΚΙΑ\.", "{} δισκία "),
        (r"{} ΔΙΣΚΙΑ\b", "{} δισκία "),
        (r"{}ΔΙΣΚΙΑ\b", "{} δισκία "),
        (r"{}cm\.", "{} cm "),
        (r"{}cm\b", "{} cm "),
        (r"{}εκ\.", "{} cm "),
        (r"{}εκ\b", "{} cm "),
        (r"{} εκ\.", "{} cm "),
        (r"{} εκ\b", "{} cm "),
        (r"{} Cm\b", "{} cm "),
        (r"{} CM\b", "{} cm "),
        (r"{}mm\.", "{} mm "),
        (r"{}mm\b", "{} mm "),
        (r"{}χιλ\.", "{} mm "),
        (r"{}χιλ\b", "{} mm "),
        (r"{} χιλ\.", "{} mm "),
        (r"{} χιλ\b", "{} mm "),
        (r"{} Mm\b", "{} mm "),
        (r"{} MM\b", "{} mm "),
        (r"{}m\.", "{} m "),
        (r"{}m\b", "{} m "),
        (r"{}μ\.", "{} m "),
        (r"{}μ\b", "{} m "),
        (r"{} μ\.", "{} m "),
        (r"{} μ\b", "{} m"),  
        # (r"οίνος ", "Κρασί "),
        # (r"οινος ", "Κρασί "),
        # (r"οίνο ", "Κρασί "),
        (r"κρασσι ", "Κρασί "),
        (r"κρασσί ", "Κρασί "),
        (r"κρασί ", "Κρασί "),
        (r"κρασι ", "Κρασί "),
        (r"&amp;", "&"), 
        (r" Στον ", " στον "),
        (r" Στο ", " στο "),
        (r" Στης ", " στης "),
        (r" Στου ", " στου "),                
        (r" Στην ", " στην "),
        (r" Στη ", " στη "),        
        (r" Στα ", " στα "),
        (r" Στις ", " στις "),
        (r" Στους ", " στους "),
        (r" Στων ", " στων "),
        (r" Για ", " για "),
        (r" Των ", " των "),
        (r" Της ", " της "),
        (r" Του ", " του "),
        (r" Την ", " την "),
        (r" Τον ", " τον "),
        (r" Το ", " το "),
        (r" Από ", " από "),
        (r" Σε ", " σε "),
        (r" Που ", " που "),
        (r" Τον ", " τον "),
        (r" Χωρίς ", " χωρίς "),
        (r" χωρις ", " χωρίς "),        
        (r" Και ", " και "),
        (r" Με ", " με "),        
        (r" Ή ", " ή "),
        (r"'S\b", "'s"),
        (r" \.", " "),
        (r" \)", ")"),
        (r"\( ", "("),
        (r"`", "'")
    ]
    
    pattern_counters = [0] * len(patterns)

    for digit1 in range(10):
        for digit2 in range(10):
            for i, (pattern, replacement) in enumerate(patterns):
                # checking if the pattern has two placeholders, otherwise use only one
                if "{}" in pattern and pattern.count("{}") == 2:
                    regex = re.compile(pattern.format(digit1, digit2), re.IGNORECASE)
                    new_text = regex.sub(lambda match: replacement.format(digit1, digit2).lower(), text)
                elif "{}" in pattern and pattern.count("{}") == 1:
                    regex = re.compile(pattern.format(digit1), re.IGNORECASE)
                    new_text = regex.sub(lambda match: replacement.format(digit1).lower(), text)
                else:
                    regex = re.compile(pattern, re.IGNORECASE)
                    new_text = regex.sub(replacement, text)
                
                if new_text != text:
                    pattern_counters[i] += 1
                text = new_text

    # # logic to handle negative amounts like "-0,30" ensuring we don't duplicate symbols
    # text = re.sub(r"-(\d{1,2},\d{1,2})€", r"-\1€", text)  # Keep original if already formatted correctly
    
    # # converting ml to liters
    # # uncomment the blocks below if you want to perform ml-to-l conversion
    # def convert_ml_to_l(match):
    #     ml_value = float(match.group(1))
    #     l_value = ml_value / 1000
    #     # Format result to 2 decimal places if needed, remove trailing zeroes
    #     return f"{l_value:.2f}".rstrip('0').rstrip('.') + " l"
    # text = re.sub(r"(\d+(\.\d+)?)\s*ml\b", convert_ml_to_l, text)

    # trim whitespace ]
    text = re.sub(r'  +', ' ', text)
    text = text.strip()
    
    return text

def extract_weight(text):
    match = re.search(r"(\d+\.\d+|\d+) g", text)
    return match.group(1) if match else None

def extract_volume(text):
    match = re.search(r"(\d+\.\d+|\d+) ml", text)
    return match.group(1) if match else None

# paste our csv file's name including the extension .csv 
input_name = "store.csv"

input_csv = os.path.join(downloads_dir, f"{input_name}")
df = pd.read_csv(input_csv)

# include more columns names that we want to convert as: [, 'description']
columns_to_process = ['name'] 

# uncomment below, *ONLY* if u want to convert ALL columns / the entire csv
# columns_to_process = df.columns

pattern_counters = [0] * len(columns_to_process)

for col in columns_to_process:
    df[col] = [replace_patterns(str(x), pattern_counters) if isinstance(x, str) else x for x in tqdm(df[col], desc=f'processing column: {col}')]

df['weight_in_grams'] = df['name'].apply(extract_weight)
df['volume_in_ml'] = df['name'].apply(extract_volume)

# choose the output csv file's name including the extension .csv 
output_name = "store_replaced.csv"

output_csv = os.path.join(downloads_dir, f"{output_name}")
df.to_csv(output_csv, index=False)

print("unmatched patterns count per digit pair:")
for i, count in enumerate(pattern_counters):
    if count > 0:
        print(f"pattern {i}: {count} unmatched occurrences")

print(f"quanx replacements + additions ARE done and saved to {output_csv}")
