from tba_codec_x509_logotype import decode_subject_logotype


def decode_extension(*, extension_der):
    """Supply caller-owned integration inputs; this definition does not execute a deployment."""
    subject = decode_subject_logotype(extension_der)
    if subject is not None:
        for image in subject.images:
            print(image.media_type, image.uris)
