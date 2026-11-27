import DOMPurify from "dompurify"

export function motdLines(status) {
  const lines = status?.motd?.html ?? []
  return lines.map((line) =>
    //check and clean motd since they're in html
    DOMPurify.sanitize(line, {
      ALLOWED_TAGS: ["span", "b", "i", "u", "s", "em", "strong"],
      ALLOWED_ATTR: ["style"],
    }),
  )
}
