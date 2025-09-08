import os
from datetime import datetime, timedelta, timezone
from enum import Enum
from pathlib import Path

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

from omnirec.util import util

# TODO: Change key/value when whe have a name
CERT_DIR = Path(os.environ.get("OMNIREC_CERT_PATH", Path.home() / ".omnirec/certs"))
CERT_DIR.mkdir(exist_ok=True, parents=True)

logger = util._root_logger.getChild("cert")


class Side(str, Enum):
    Server = "server"
    Client = "client"


def create_and_sign_cert() -> tuple[rsa.RSAPrivateKey, x509.Certificate]:
    key = rsa.generate_private_key(65537, 2048)

    subject = issuer = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "localhost")])

    utc_now = datetime.now(timezone.utc)

    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(utc_now)
        .not_valid_after(utc_now + timedelta(days=365))
        .sign(key, hashes.SHA256())
    )

    return key, cert


def _create_new(name: str, key_pth: Path, cert_pth: Path):
    logger.info(f"Generating new {name} key and certificate...")
    key, cert = create_and_sign_cert()

    with open(key_pth, "wb") as f:
        logger.debug(f"Writing key to {key_pth}")
        f.write(
            key.private_bytes(
                serialization.Encoding.PEM,
                serialization.PrivateFormat.TraditionalOpenSSL,
                serialization.NoEncryption(),
            )
        )
        logger.debug("Done.")

    with open(cert_pth, "wb") as f:
        logger.debug(f"Writing certificate to {cert_pth}")
        f.write(cert.public_bytes(serialization.Encoding.PEM))
        logger.debug("Done.")


def get_key_pth(side: Side) -> Path:
    return (CERT_DIR / f"{side.value}-key.pem").resolve()


def get_cert_pth(side: Side) -> Path:
    return (CERT_DIR / f"{side.value}-cert.pem").resolve()


def ensure_certs():
    for side in Side:
        key_pth = get_key_pth(side)
        cert_pth = get_cert_pth(side)

        if not key_pth.exists():
            logger.info(f"{side.capitalize()} key file missing!")
        else:
            logger.debug(f"Found {side} key file at {key_pth}!")

        if not cert_pth.exists():
            logger.info(f"{side.capitalize()} certificate file missing!")
        else:
            logger.debug(f"Found {side} certificate file at {cert_pth}!")

        if not key_pth.exists() or not cert_pth.exists():
            _create_new(side, key_pth, cert_pth)
        else:
            with open(cert_pth, "rb") as f:
                cert = x509.load_pem_x509_certificate(f.read())
                utc_now = datetime.now(timezone.utc)

                if cert.not_valid_before_utc <= utc_now <= cert.not_valid_after_utc:
                    logger.debug(f"{side.capitalize()} key and certificate file OK!")
                else:
                    logger.info(f"{side.capitalize()} certificate expired! Renewing...")
                    _create_new(side, key_pth, cert_pth)
