from django.core.management.base import BaseCommand
from books.models import Book


class Command(BaseCommand):
    help = 'Populate database with sample books'

    def handle(self, *args, **kwargs):
        books_data = [
            {
                'title': 'The Great Gatsby',
                'author': 'F. Scott Fitzgerald',
                'isbn': '9780743273565',
                'description': 'Một tiểu thuyết kinh điển của Mỹ về thời đại Jazz, khám phá những chủ đề về giàu có, tình yêu và giấc mơ Mỹ.',
                'cover_image': 'https://covers.openlibrary.org/b/isbn/9780743273565-L.jpg',
                'category': 'Tiểu Thuyết',
                'publication_year': 1925,
                'rental_price_per_day': 25,
                'available_copies': 5,
                'total_copies': 5,
                'rating': 4.5,
                'is_trending': True,
                'is_new': False,
            },
            {
                'title': '1984',
                'author': 'George Orwell',
                'isbn': '9780451524935',
                'description': 'Tiểu thuyết khoa học viễn tưởng phản địa đàng và câu chuyện cảnh báo về chủ nghĩa toàn trị.',
                'cover_image': 'https://covers.openlibrary.org/b/isbn/9780451524935-L.jpg',
                'category': 'Khoa Học Viễn Tưởng',
                'publication_year': 1949,
                'rental_price_per_day': 30,
                'available_copies': 3,
                'total_copies': 3,
                'rating': 4.7,
                'is_trending': True,
                'is_new': False,
            },
            {
                'title': 'To Kill a Mockingbird',
                'author': 'Harper Lee',
                'isbn': '9780061120084',
                'description': 'Một câu chuyện hấp dẫn về bất công chủng tộc và sự ngây thơ của tuổi thơ ở miền Nam nước Mỹ.',
                'cover_image': 'https://covers.openlibrary.org/b/isbn/9780061120084-L.jpg',
                'category': 'Tiểu Thuyết',
                'publication_year': 1960,
                'rental_price_per_day': 28,
                'available_copies': 4,
                'total_copies': 4,
                'rating': 4.8,
                'is_trending': True,
                'is_new': True,
            },
            {
                'title': 'Pride and Prejudice',
                'author': 'Jane Austen',
                'isbn': '9780141439518',
                'description': 'Tiểu thuyết lãng mạn về phong tục tập quán, phê phán tầng lớp địa chủ Anh vào cuối thế kỷ 18.',
                'cover_image': 'https://covers.openlibrary.org/b/isbn/9780141439518-L.jpg',
                'category': 'Lãng Mạn',
                'publication_year': 1813,
                'rental_price_per_day': 23,
                'available_copies': 6,
                'total_copies': 6,
                'rating': 4.6,
                'is_trending': False,
                'is_new': True,
            },
            {
                'title': 'The Hobbit',
                'author': 'J.R.R. Tolkien',
                'isbn': '9780547928227',
                'description': 'Một cuộc phiêu lưu kỳ ảo về hành trình bất ngờ của người hobbit để giành lại kho báu được canh giữ bởi một con rồng.',
                'cover_image': 'https://covers.openlibrary.org/b/isbn/9780547928227-L.jpg',
                'category': 'Kỳ Ảo',
                'publication_year': 1937,
                'rental_price_per_day': 35,
                'available_copies': 4,
                'total_copies': 4,
                'rating': 4.7,
                'is_trending': True,
                'is_new': True,
            },
            {
                'title': 'Harry Potter and the Sorcerer\'s Stone',
                'author': 'J.K. Rowling',
                'isbn': '9780439708180',
                'description': 'Khởi đầu kỳ diệu của hành trình Harry Potter tại trường Phù thủy và Pháp sư Hogwarts.',
                'cover_image': 'https://covers.openlibrary.org/b/isbn/9780439708180-L.jpg',
                'category': 'Kỳ Ảo',
                'publication_year': 1997,
                'rental_price_per_day': 32,
                'available_copies': 8,
                'total_copies': 8,
                'rating': 4.9,
                'is_trending': True,
                'is_new': False,
            },
            {
                'title': 'The Lord of the Rings',
                'author': 'J.R.R. Tolkien',
                'isbn': '9780544003415',
                'description': 'Cuộc phiêu lưu kỳ ảo sử thi theo hành trình phá hủy Chiếc Nhẫn Chí Tôn.',
                'cover_image': 'https://covers.openlibrary.org/b/isbn/9780544003415-L.jpg',
                'category': 'Kỳ Ảo',
                'publication_year': 1954,
                'rental_price_per_day': 40,
                'available_copies': 3,
                'total_copies': 3,
                'rating': 4.9,
                'is_trending': True,
                'is_new': False,
            },
            {
                'title': 'The Catcher in the Rye',
                'author': 'J.D. Salinger',
                'isbn': '9780316769174',
                'description': 'Câu chuyện về sự nổi loạn và sự xa lánh của tuổi teen được kể bởi Holden Caulfield biểu tượng.',
                'cover_image': 'https://covers.openlibrary.org/b/isbn/9780316769174-L.jpg',
                'category': 'Tiểu Thuyết',
                'publication_year': 1951,
                'rental_price_per_day': 23,
                'available_copies': 0,
                'total_copies': 3,
                'rating': 4.3,
                'is_trending': False,
                'is_new': False,
            },
            {
                'title': 'Brave New World',
                'author': 'Aldous Huxley',
                'isbn': '9780060850524',
                'description': 'Tiểu thuyết phản địa đàng về một xã hội tương lai được kiểm soát bằng công nghệ và thuốc.',
                'cover_image': 'https://covers.openlibrary.org/b/isbn/9780060850524-L.jpg',
                'category': 'Khoa Học Viễn Tưởng',
                'publication_year': 1932,
                'rental_price_per_day': 27,
                'available_copies': 5,
                'total_copies': 5,
                'rating': 4.4,
                'is_trending': False,
                'is_new': True,
            },
            {
                'title': 'The Alchemist',
                'author': 'Paulo Coelho',
                'isbn': '9780062315007',
                'description': 'Câu chuyện ấm áp về một chàng chăn cừu trẻ đi tìm kho báu và khám phá bản thân.',
                'cover_image': 'https://covers.openlibrary.org/b/isbn/9780062315007-L.jpg',
                'category': 'Tiểu Thuyết',
                'publication_year': 1988,
                'rental_price_per_day': 26,
                'available_copies': 7,
                'total_copies': 7,
                'rating': 4.5,
                'is_trending': True,
                'is_new': True,
            },
        ]

        created_count = 0
        updated_count = 0
        for book_data in books_data:
            book, created = Book.objects.get_or_create(
                isbn=book_data['isbn'],
                defaults=book_data
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Đã tạo: {book.title}'))
            else:
                # Cập nhật các trường mới
                for key, value in book_data.items():
                    setattr(book, key, value)
                book.save()
                updated_count += 1
                self.stdout.write(self.style.WARNING(f'↻z Đã cập nhật: {book.title}'))

        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Hoàn thành! Đã tạo {created_count} sách mới và cập nhật {updated_count} sách.'
        ))