

# Giả lập lấy dữ liệu từ Database
class UserService:
    def get_all(self) -> list[dict]:
        return [{"id": 1, "username": "kienpt", "role": "admin"}]