# IMDB API Clone With DRF

## 🔗 Final Project Links (Arranged According To Usage)

### 1. Admin Access

- **Admin Section:** [Dashboard](http://127.0.0.1:8000/dashboard/)

### 2. Accounts

- **Registration:** [Register](http://127.0.0.1:8000/api/account/register/)
- **Login:** [Login](http://127.0.0.1:8000/api/account/login/)
- **Logout:** [Logout](http://127.0.0.1:8000/api/account/logout/)

### 3. Stream Platforms

- **Create & Access List:** [Stream Platforms](http://127.0.0.1:8000/api/watch/stream/)
- **Access, Update & Delete Individual:** `http://127.0.0.1:8000/api/watch/stream/<int:streamplatform_id>/`

### 4. Watch List

- **Create & Access List:** [Watch List](http://127.0.0.1:8000/api/watch/)
- **Access, Update & Delete Individual:** `http://127.0.0.1:8000/api/watch/<int:movie_id>/`

### 5. Reviews

- **Create Review For A Movie:** `http://127.0.0.1:8000/api/watch/<int:movie_id>/reviews/create/`
- **List All Reviews For A Movie:** `http://127.0.0.1:8000/api/watch/<int:movie_id>/reviews/`
- **Access, Update & Delete A Review:** `http://127.0.0.1:8000/api/watch/reviews/<int:review_id>/`

### 6. User Reviews

- **Access All Reviews For A Specific User:** `http://127.0.0.1:8000/api/watch/user-reviews/?username=example`
