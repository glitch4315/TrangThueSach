from django.core.management.base import BaseCommand
from pymongo import MongoClient


class Command(BaseCommand):
    help = 'Populate database using pymongo directly'

    def handle(self, *args, **kwargs):
        # Kết nối trực tiếp
        client = MongoClient('localhost', 27017)
        db = client['bookrental_db']

        # Xóa collection cũ
        db.books.drop()
        self.stdout.write('Đã xóa collection books')

        books_data = [
            {
                'title': 'The Great Gatsby',
                'author': 'F. Scott Fitzgerald',
                'isbn': '9780743273565',
                'description': 'Một tiểu thuyết kinh điển của Mỹ về thời đại Jazz.',
                'cover_image': 'https://covers.openlibrary.org/b/isbn/9780743273565-L.jpg',
                'category': 'Tiểu Thuyết',
                'publication_year': 1925,
                'rental_price_per_day': 25.0,
                'available_copies': 5,
                'total_copies': 5,
                'rating': 4.5,
                'is_trending': 1,
                'is_new': 0,
                'views': 1250,
            },
            {
                'title': '1984',
                'author': 'George Orwell',
                'isbn': '9780451524935',
                'description': 'Tiểu thuyết khoa học viễn tưởng phản địa đàng.',
                'cover_image': 'https://covers.openlibrary.org/b/isbn/9780451524935-L.jpg',
                'category': 'Khoa Học Viễn Tưởng',
                'publication_year': 1949,
                'rental_price_per_day': 30.0,
                'available_copies': 3,
                'total_copies': 3,
                'rating': 4.7,
                'is_trending': 1,
                'is_new': 0,
                'views': 1980,
            },
            {
                'title': 'Harry Potter',
                'author': 'J.K. Rowling',
                'isbn': '9780439708180',
                'description': 'Khởi đầu kỳ diệu của hành trình Harry Potter.',
                'cover_image': 'https://covers.openlibrary.org/b/isbn/9780439708180-L.jpg',
                'category': 'Kỳ Ảo',
                'publication_year': 1997,
                'rental_price_per_day': 32.0,
                'available_copies': 8,
                'total_copies': 8,
                'rating': 4.9,
                'is_trending': 1,
                'is_new': 0,
                'views': 3200,
            },
            {
                'title': 'To Kill a Mockingbird',
                'author': 'Harper Lee',
                'isbn': '9780061120084',
                'description': 'Một câu chuyện hấp dẫn về bất công chủng tộc.',
                'cover_image': 'https://covers.openlibrary.org/b/isbn/9780061120084-L.jpg',
                'category': 'Tiểu Thuyết',
                'publication_year': 1960,
                'rental_price_per_day': 28.0,
                'available_copies': 4,
                'total_copies': 4,
                'rating': 4.8,
                'is_trending': 1,
                'is_new': 1,
                'views': 1650,
            },
            {
                'title': 'The Hobbit',
                'author': 'J.R.R. Tolkien',
                'isbn': '9780547928227',
                'description': 'Một cuộc phiêu lưu kỳ ảo của người hobbit.',
                'cover_image': 'https://covers.openlibrary.org/b/isbn/9780547928227-L.jpg',
                'category': 'Kỳ Ảo',
                'publication_year': 1937,
                'rental_price_per_day': 35.0,
                'available_copies': 4,
                'total_copies': 4,
                'rating': 4.7,
                'is_trending': 1,
                'is_new': 1,
                'views': 1420,
            },
            {
                'title': 'Pride and Prejudice',
                'author': 'Jane Austen',
                'isbn': '9780141439518',
                'description': 'Tiểu thuyết lãng mạn về phong tục tập quán.',
                'cover_image': 'https://covers.openlibrary.org/b/isbn/9780141439518-L.jpg',
                'category': 'Lãng Mạn',
                'publication_year': 1813,
                'rental_price_per_day': 23.0,
                'available_copies': 6,
                'total_copies': 6,
                'rating': 4.6,
                'is_trending': 0,
                'is_new': 1,
                'views': 1580,
            },
            {
                'title': 'The Lord of the Rings',
                'author': 'J.R.R. Tolkien',
                'isbn': '9780544003415',
                'description': 'Cuộc phiêu lưu kỳ ảo sử thi.',
                'cover_image': 'https://covers.openlibrary.org/b/isbn/9780544003415-L.jpg',
                'category': 'Kỳ Ảo',
                'publication_year': 1954,
                'rental_price_per_day': 40.0,
                'available_copies': 3,
                'total_copies': 3,
                'rating': 4.9,
                'is_trending': 1,
                'is_new': 0,
                'views': 2800,
            },
            {
                'title': 'Brave New World',
                'author': 'Aldous Huxley',
                'isbn': '9780060850524',
                'description': 'Tiểu thuyết phản địa đàng về tương lai.',
                'cover_image': 'https://covers.openlibrary.org/b/isbn/9780060850524-L.jpg',
                'category': 'Khoa Học Viễn Tưởng',
                'publication_year': 1932,
                'rental_price_per_day': 27.0,
                'available_copies': 5,
                'total_copies': 5,
                'rating': 4.4,
                'is_trending': 0,
                'is_new': 1,
                'views': 1100,
            },
            {
                'title': 'The Alchemist',
                'author': 'Paulo Coelho',
                'isbn': '9780062315007',
                'description': 'Câu chuyện về chàng chăn cừu tìm kho báu.',
                'cover_image': 'https://covers.openlibrary.org/b/isbn/9780062315007-L.jpg',
                'category': 'Tiểu Thuyết',
                'publication_year': 1988,
                'rental_price_per_day': 26.0,
                'available_copies': 7,
                'total_copies': 7,
                'rating': 4.5,
                'is_trending': 1,
                'is_new': 1,
                'views': 2650,
            },
            {
                'title': 'The Catcher in the Rye',
                'author': 'J.D. Salinger',
                'isbn': '9780316769174',
                'description': 'Câu chuyện về sự nổi loạn tuổi teen.',
                'cover_image': 'https://covers.openlibrary.org/b/isbn/9780316769174-L.jpg',
                'category': 'Tiểu Thuyết',
                'publication_year': 1951,
                'rental_price_per_day': 23.0,
                'available_copies': 0,
                'total_copies': 3,
                'rating': 4.3,
                'is_trending': 0,
                'is_new': 0,
                'views': 890,
            },
        ]

        # Insert tất cả
        result = db.books.insert_many(books_data)

        self.stdout.write(self.style.SUCCESS(f'✅ Đã tạo {len(result.inserted_ids)} sách!'))

        # Verify
        count = db.books.count_documents({})
        self.stdout.write(self.style.SUCCESS(f'📚 Tổng: {count} sách trong database'))

        # Hiển thị một vài sách
        self.stdout.write('\n📖 Sách đã thêm:')
        for book in db.books.find().limit(3):
            self.stdout.write(f"  - {book['title']} (ID: {book['_id']})")