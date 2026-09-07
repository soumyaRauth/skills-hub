export function AssistantReply({ reply }) {
  return <div className="reply" dangerouslySetInnerHTML={{ __html: reply }} />
}
