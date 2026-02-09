import pandas as pd

def clean_data(df):
    # Drop column: 'product_link'
    df = df.drop(columns=['product_link'])
    # Drop column: 'img_link'
    df = df.drop(columns=['img_link'])
    # Drop column: 'review_content'
    df = df.drop(columns=['review_content'])
    # Drop column: 'review_id'
    df = df.drop(columns=['review_id'])
    # Drop column: 'about_product'
    df = df.drop(columns=['about_product'])
    # Fix non-numeric values in 'rating' column
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    # Categorize ratings into descriptive levels
    def categorize_rating(rating):
        if rating >= 4.5:
            return 4  # Best
        elif rating >= 4.0:
            return 3  # Good
        elif rating >= 3.5:
            return 2  # Average
        elif rating >= 2.5:
            return 1  # Not Good
        else:
            return -1  # Worse
    # Apply the categorization function to the 'rating' column
    df['rating_category'] = df['rating'].apply(categorize_rating)
    # Drop column: 'product_name'
    df = df.drop(columns=['product_name'])
    # Calculate selling price by subtracting discounted price from actual price
    df['selling_price'] = (
        df['actual_price'].replace('[₹,]', '', regex=True).astype(float) -
        df['discounted_price'].replace('[₹,]', '', regex=True).astype(float)
    )
    # Fix ValueError by removing commas
    df['discount_percentage_calculated'] = (
        df['discounted_price']
        .str.replace('₹', '', regex=False)
        .str.replace(',', '', regex=False)
        .astype(float) /
        df['actual_price']
        .str.replace('₹', '', regex=False)
        .str.replace(',', '', regex=False)
        .astype(float)
    ) * 100
    # Drop column: 'discount_percentage'
    df = df.drop(columns=['discount_percentage'])
    # Group data into categories and add a new column 'grouped_category'
    df['grouped_category'] = df['category'].apply(
        lambda x: 'Cables' if 'Cables' in x else
                  'Mouse' if 'Mouse' in x else
                  'Phone/Mobile Accessories' if 'Phone' in x or 'Mobile' in x else
                  'Networking Devices' if 'Networking' in x else
                  'TVs' if 'Televisions' in x else
                  'TV Accessories' if 'Accessories' in x and 'TV' in x else
                  'Audio' if 'Audio' in x else
                  'Wearables' if 'Wearable' in x else
                  'Storage' if 'Storage' in x else
                  'Office Supplies' if 'Office' in x else
                  'Home & Kitchen' if 'Home' in x or 'Kitchen' in x else
                  'Sports & Fitness' if 'Sports' in x else
                  'Toys & Games' if 'Toys' in x else
                  'Health & Personal Care' if 'Health' in x else
                  'Automotive' if 'Automotive' in x else
                  'Other'
    )
    # Drop column: 'category'
    df = df.drop(columns=['category'])
    return df

# Loaded variable 'df' from URI: c:\Users\Ankush Arora\OneDrive\Desktop\amazon.csv
df = pd.read_csv(r'c:\Users\Ankush Arora\OneDrive\Desktop\amazon.csv')

df_clean = clean_data(df.copy())
df_clean.head()