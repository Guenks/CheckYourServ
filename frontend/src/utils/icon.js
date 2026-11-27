export function iconOf(status) {
  const icon = status?.icon
  //only accept PNG or data URI (Bedrock servers have no icon)
  return typeof icon === "string" && icon.startsWith("data:image/png;base64,") ? icon : null
}
