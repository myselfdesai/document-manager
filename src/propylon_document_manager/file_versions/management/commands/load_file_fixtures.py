from django.core.management.base import BaseCommand, CommandError
from propylon_document_manager.file_versions.models import FileVersion
from cryptography.hazmat.primitives import hashes
import base64

def generate_random_hash():
    digest = hashes.Hash(hashes.SHA256())
    random_bytes = bytearray(os.urandom(32))  # Assuming 32 bytes for SHA256
    digest.update(random_bytes)
    return base64.b64encode(digest.finalize()).decode()

file_versions = [
    'bill_document',
    'amendment_document',
    'act_document',
    'statute_document',
]

class Command(BaseCommand):
    help = "Load basic file version fixtures with random hashcodes"

    def handle(self, *args, **options):
        for file_name in file_versions:
            # Generate random hash using cryptography
            content_hash = generate_random_hash()

            FileVersion.objects.create(
                file_name=file_name,
                content_hash=content_hash,
                version_number=1,
                user=1
            )

        self.stdout.write(
            self.style.SUCCESS('Successfully created %s file versions with random hashcodes' % len(file_versions))
        )
