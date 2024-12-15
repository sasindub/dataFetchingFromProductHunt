import requests  # For making API calls
import pandas as pd  # For saving data to CSV

# Step 1: Set up API details
API_KEY = "hs77mjbIP7HJqr19newLV5Yzs1hdv-N3w8gHf2dCnuM"  # Replace with your API key
BASE_URL = "https://api.producthunt.com/v2/api/graphql"  # ProductHunt GraphQL endpoint

next_cursor = None
products = []

while True:
    query = f"""
    {{
      posts(first: 100, after: "{next_cursor if next_cursor else ''}", where: {{topic: "Artificial Intelligence"}}) {{
        edges {{
          cursor
          node {{
            name
            description
            createdAt
            votesCount
            commentsCount
            topics {{
              edges {{
                node {{
                  name
                }}
              }}
            }}
          }}
        }}
        pageInfo {{
          hasNextPage
          endCursor
        }}
      }}
    }}
    """

    
    # Step 3: Set up headers for the API request
    headers = {
        "Authorization": f"Bearer {API_KEY}",  # Add the API key for authentication
        "Content-Type": "application/json"  # Specify the content type
    }


    response = requests.post(BASE_URL, headers=headers, json={"query": query})
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        break

    data = response.json()
    for edge in data['data']['posts']['edges']:
        product = edge['node']
        # Process and save the product data here
        products.append({
            "Name": product['name'],
            "Description": product['description'],
            "Created At": product['createdAt'],
            "Votes": product['votesCount'],
            "Comments": product['commentsCount'],
            "Topics": ", ".join([t['node']['name'] for t in product['topics']['edges']])
        })

    # Check if there are more pages
    if data['data']['posts']['pageInfo']['hasNextPage']:
        next_cursor = data['data']['posts']['pageInfo']['endCursor']
    else:
        break

# Save to CSV after fetching all pages
pd.DataFrame(products).to_csv("ai_products.csv", index=False)
print("All data saved to ai_products.csv")
