import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

def generate_optimized_eda():   
    data_path = Path('./data/dataset.csv')
    if not data_path.exists():
        raise FileNotFoundError(f"Nepp, inget dataset här inte {data_path}")
    
    df = pd.read_csv(data_path)
    
    features_to_keep = [
        'having_IPhaving_IP_Address', 'URLURL_Length', 'having_At_Symbol', 
        'double_slash_redirecting', 'Prefix_Suffix', 'having_Sub_Domain', 
        'HTTPS_token', 'DNSRecord', 'SSLfinal_State', 'Redirect', 
        'Shortining_Service', 'Result'
    ]
    
    df_optimized = df[features_to_keep]  
    output_dir = Path('./plots')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    plt.figure(figsize=(14, 10))
    
    correlation_matrix = df_optimized.corr()
    
    sns.heatmap(
        correlation_matrix, 
        annot=True,      
        fmt=".2f",          
        cmap="coolwarm",
        linewidths=0.5, 
        square=True
    )
    
    plt.title("Reduced correlation heatmap matrix", fontsize=14, pad=20)
    plt.tight_layout()
    
    save_path = output_dir / 'correlation_heatmap_optimized_clean.png'
    plt.savefig(save_path, dpi=300)
    plt.close()

if __name__ == "__main__":
    generate_optimized_eda()