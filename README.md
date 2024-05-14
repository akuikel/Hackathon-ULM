# <h1>Lost and Found Application</h1>

This project was built for a hackathon and we scored second place. The Lost and Found Application is a community-driven platform designed to help users find lost items or report found items. It includes a variety of features to facilitate item recovery and user interaction.

## <h2>About L&F</h2>

L&F is a social community aimed at helping people find their lost items or report found items. Users can:
- Post about lost or found items.
- Browse the L&F feed to check listings.
- Claim lost items or mark found items as theirs.
- View the history of their posts and claims.
- Use the messaging feature for further confirmation of claims.

## <h2>Features</h2>

### <h3>Authentication</h3>
- **Register**: New users can register with a username, password, email, and phone number.
- **Login/Logout**: Users can log in with their username and password and log out from the navbar.
  
<img width="1439" alt="Screenshot 2024-05-14 at 11 50 34 AM" src="https://github.com/akuikel/Hackathon-ULM/assets/108853044/0b803b2d-503e-418e-a8f4-a6b84dd87c5d">

### <h3>Listings</h3>
- **L&F Index Page**: Displays all listings sorted by date, showing details like type, category, title, description, date, location, status, contact email, and the user who made the post.
- **Filter and Search**: Users can filter posts by type and category, and search by the post title.
  
<img width="1439" alt="Screenshot 2024-05-14 at 11 51 07 AM" src="https://github.com/akuikel/Hackathon-ULM/assets/108853044/3ee91fef-73a6-40b3-9f89-d4f94d243afc">

### <h3>Posting and Claiming</h3>
- **Post New Item**: Users can create new posts about lost or found items, including a photo, location, title, description, and last seen location.
- **Claim Item**: Users can claim items, providing photo proof and a message to the original poster.
- **Cancel Claim**: Users can cancel their claims if necessary.
- **Deny Claim**: Posters can deny claim requests if the proof is invalid.

<img width="1439" alt="Screenshot 2024-05-14 at 11 51 30 AM" src="https://github.com/akuikel/Hackathon-ULM/assets/108853044/4229cd6b-1d5c-4193-9fec-cb5af004bed4">
<img width="1439" alt="Screenshot 2024-05-14 at 11 51 50 AM" src="https://github.com/akuikel/Hackathon-ULM/assets/108853044/5818d55e-9300-4e22-968f-b161d2dd0460">
<img width="1439" alt="Screenshot 2024-05-14 at 12 07 19 PM" src="https://github.com/akuikel/Hackathon-ULM/assets/108853044/6f860e7d-7f79-4319-897f-2bab5db45d32">



### <h3>History and Messaging</h3>
- **History**: Displays posts and claims made by the logged-in user, allowing them to manage their activities.
- **Messages**: Users can chat about items through claim and chat messages.

<img width="1439" alt="Screenshot 2024-05-14 at 12 10 32 PM" src="https://github.com/akuikel/Hackathon-ULM/assets/108853044/f29141aa-6f49-44a2-93a4-f1b4f72e03b2">
<img width="1439" alt="Screenshot 2024-05-14 at 11 52 35 AM" src="https://github.com/akuikel/Hackathon-ULM/assets/108853044/902a70f3-b052-4a04-b5cd-a433f8ec3381">


### <h3>Additional Features</h3>
- **About and Disclaimer Pages**: Provide general information and disclaimers about the L&F community.
- **UI & UX Enhancements**: Includes flash messages, JavaScript confirmations, and a blue-themed interface built with Bootstrap.

## <h2>Project Inspiration</h2>

Inspired by personal experiences and Facebook groups, this project addresses the need for a dedicated platform to handle lost and found items efficiently, with features like status updates and dedicated claim management.

## <h2>Challenges and Future Updates</h2>

### <h3>Challenges</h3>
- Implementing image upload functionality for posts and claims.

### <h3>Future Updates</h3>
- Sub-categories for more specific item classification.
- Location-based API integration for post creation.
- Account and privacy settings, user profiles, and roles.
- Mobile-friendly design and secure image handling.

## <h2>Technologies Used</h2>

### <h3>Languages</h3>
- Python
- HTML
- JavaScript
- CSS
- SQL

### <h3>Platforms and Libraries</h3>
- Flask
- SQLite
- Jinja

## <h2>Setup</h2>

### <h3>1. Install Python</h3>
Make sure you have Python 3.x installed. You can download it from the official Python website: [Python Downloads](https://www.python.org/downloads/)

### <h3>2. Clone the repository</h3>
<ol>
    <li><strong>Install Python:</strong>
    <p>Download and install Python 3.x from the official website: <a href="https://www.python.org/downloads/">https://www.python.org/downloads/</a>.</p></li>
    <li><strong>Clone the repository:</strong>
    <pre><code>git clone https://github.com/yourusername/Hackathon-ULM
cd Hackathon-ULM
</code></pre></li>
    <li><strong>Create and activate a virtual environment:</strong>
    <pre><code>python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
</code></pre></li>
    <li><strong>Install the required packages:</strong>
    <pre><code>pip install flask flask_sqlalchemy
</code></pre></li>
    <li><strong>Set up the database:</strong>
    <pre><code>python
from app import db
db.create_all()
</code></pre></li>
    <li><strong>Run the application:</strong>
    <pre><code>python app.py
</code></pre></li>
    <li><strong>Access the application:</strong>
    Open your web browser and navigate to <a href="http://127.0.0.1:5000/">http://127.0.0.1:5000/</a>.
    </li>
</ol>
