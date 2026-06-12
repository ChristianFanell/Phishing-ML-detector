import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def generate_eda_plots():
    df = pd.read_csv('./data/dataset.csv')
    output_dir = Path('./plots')
    output_dir.mkdir(parents=True, exist_ok=True)

    sns.set_theme(style="whitegrid")

    print("2. Generating Correlation Heatmap...")
    plt.figure(figsize=(14, 12))
    
    corr = df.corr()
    
    # heatmap, red = positive correlation, blue = negative correlation
    sns.heatmap(corr, cmap="coolwarm", center=0, annot=False, 
                linewidths=.5, cbar_kws={"shrink": .8}) 
    plt.title('Feature Correlation Matrix', fontsize=18, pad=20)
    plt.tight_layout()
    plt.savefig(output_dir / 'correlation_heatmap.png', dpi=300) 
    plt.close()


    plt.figure(figsize=(8, 6))
    ax = sns.countplot(x='Result', data=df, palette='viridis')
    plt.title('Distribution of Legitimate (1) vs Phishing (-1) Sites', fontsize=14, pad=15)
    plt.xlabel('Result Class', fontsize=12)
    plt.ylabel('Total Count', fontsize=12)
    
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', 
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='bottom', fontsize=12, xytext=(0, 5), 
                    textcoords='offset points')
        
    plt.tight_layout()
    plt.savefig(output_dir / 'class_distribution.png', dpi=300)
    plt.close()

    plt.figure(figsize=(8, 6))    
    sns.countplot(x='Prefix_Suffix', hue='Result', data=df, palette='Set1')
    plt.title('Impact of Domain Dash (-) on Phishing', fontsize=14, pad=15)
    plt.xlabel('Prefix_Suffix Feature (-1 = Has Dash, 1 = No Dash)', fontsize=12)
    plt.ylabel('Count', fontsize=12)
    plt.legend(title='Final Result', labels=['Phishing (-1)', 'Legitimate (1)'])
    plt.tight_layout()
    plt.savefig(output_dir / 'prefix_suffix_impact.png', dpi=300)
    plt.close()


if __name__ == "__main__":
    generate_eda_plots()