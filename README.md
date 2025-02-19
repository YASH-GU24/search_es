# **search_es**  

This repository provides a **fast and efficient** search mechanism for a movies dataset using **Elasticsearch**. The search functionality is exposed through a **FastAPI** backend, allowing users to query movies based on various filters.  

---

## **Getting Started**  

### **Prerequisites**  
Ensure you have the following installed on your system:  
- [Docker](https://www.docker.com/get-started)  
- [Docker Compose](https://docs.docker.com/compose/install/)  

### **Installation & Setup**  

1. **Clone the repository**  
   ```bash
   git clone https://github.com/YASH-GU24/search_es.git
   cd search_es
   ```  
   
2. **Start the application using Docker Compose**  
   ```bash
   docker-compose up --build
   ```  
   - This command will pull necessary images, build the containers, and start the **Elasticsearch** service along with the **FastAPI** backend.  
   - Wait for all containers to initialize before making API calls.  

---

## **Usage**  

Once the services are running, you can start searching for movies using the **FastAPI API**.

### **Option 1: Using Swagger UI**  
- Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser.  
- Locate the **`/search/`** endpoint and enter your search parameters (e.g., *query*, *genre*, *director*).  
- Click **"Try it out"**, then **"Execute"** to get the search results.

### **Option 2: Using cURL**  
You can also make a request using `curl` from the terminal:  

#### **Search by keyword**  
```bash
curl "http://localhost:8000/search/?query=Horror&limit=10"
```
- Replace `"Horror"` with your desired search keyword.  
- Modify the `limit` parameter to control the number of results returned.  

#### **Search with filters**  
```bash
curl "http://localhost:8000/search/?query=Horror&genre=Thriller&director=John%20Carpenter&limit=5"
```
- Search for movies that match **Horror** in any field, **filtered** by **Thriller genre** and **directed by John Carpenter**.
- The `%20` represents a space in URLs.

---

## **API Reference**  

### **Search Endpoint**  
```http
GET /search/?query={keyword}&genre={genre}&director={director}&limit={number}
```

#### **Parameters**:  
| Parameter  | Type   | Description                                           | Example |
|------------|--------|------------------------------------------------------|---------|
| `query`    | `string` | The keyword to search for in movie details (optional) | `"Horror"` |
| `genre`    | `string` | Filter results by a specific genre (optional) | `"Thriller"` |
| `director` | `string` | Filter results by a specific director (optional) | `"Christopher Nolan"` |
| `limit`    | `int`    | Number of search results to return (default: 10) | `10` |

#### **Response Example**  
```json
{
  "results": [
    {
      "Name": "The Conjuring",
      "Genres": ["Horror", "Thriller"],
      "Actors": ["Vera Farmiga", "Patrick Wilson"],
      "Director": "James Wan",
      "Description": "Paranormal investigators help a family terrorized by a dark presence.",
      "Score": 1.23
    },
    {
      "Name": "It",
      "Genres": ["Horror", "Drama"],
      "Actors": ["Bill Skarsgård", "Finn Wolfhard"],
      "Director": "Andy Muschietti",
      "Description": "A group of kids face their biggest fears in a terrifying clown entity.",
      "Score": 1.15
    }
  ]
}
```

---

## **Error Handling**  
The API returns meaningful error messages in case of issues:  

| Status Code | Meaning |
|-------------|---------|
| `404` | Index not found in Elasticsearch |
| `400` | Elasticsearch request error (invalid parameters, etc.) |
| `500` | Internal Elasticsearch error |

---
