// Shared encoding helpers. Used by the upload client and the export job.

export function toBase64(bytes) {
  return Buffer.from(bytes).toString("base64");
}

export function fromBase64(value) {
  return Buffer.from(value, "base64");
}

export function decodeUtf8(bytes) {
  return new TextDecoder("utf-8").decode(bytes);
}
