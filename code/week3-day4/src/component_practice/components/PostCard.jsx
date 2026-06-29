export default function PostCard({ avatar, author, content }) {
  return (
    <li className="post-card">
      <div className="post-author">
        <span className="avatar">{avatar}</span>
        <strong>{author}</strong>
      </div>
      <p className="post-content">{content}</p>
    </li>
  );
}
