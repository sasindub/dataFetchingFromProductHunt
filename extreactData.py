import requests  # For making API calls
import pandas as pd  # For saving data to CSV

# Step 1: Set up API details
API_KEY = "hs77mjbIP7HJqr19newLV5Yzs1hdv-N3w8gHf2dCnuM"  # Replace with your API key
BASE_URL = "https://api.producthunt.com/v2/api/graphql"  # ProductHunt GraphQL endpoint

# Step 2: Define function to fetch posts
def fetch_posts():
    next_cursor = None
    products = []
    i = 0

    while True:
        i += i 
        print(i)
        query = f"""
        {{
          posts(first: 100{f', after: "{next_cursor}"' if next_cursor else ''}) {{
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

        # Set up headers for the API request
        headers = {
            "Authorization": f"Bearer {API_KEY}",  # Add the API key for authentication
            "Content-Type": "application/json"  # Specify the content type
        }

        response = requests.post(BASE_URL, headers=headers, json={"query": query})

        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
            break

        data = response.json()

        # Check for errors in the GraphQL response
        if "errors" in data:
            print(f"GraphQL Error: {data['errors']}")
            break

        # Validate the 'posts' data structure
        if "data" not in data or "posts" not in data["data"]:
            print("Unexpected response structure:", data)
            break

        # Process data
        for edge in data['data']['posts']['edges']:
            product = edge['node']
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
            print(i)
            break

    return products

# Step 3: Fetch and filter products
all_products = fetch_posts()

if not all_products:
    print("No products fetched.")
else:
    # Filter products related to AI or Artificial Intelligence
    ai_products = [
        product for product in all_products
        if any(topic.lower() in product['Topics'].lower() for topic in ["AI", "Artificial Intelligence"])
    ]

    # Step 4: Save the data to a CSV file
    if ai_products:
        df = pd.DataFrame(ai_products)
        df.to_csv("producthunt_ai_products.csv", index=False)
        print("AI-related products data saved to producthunt_ai_products.csv")
    else:
        print("No AI-related products found.")
