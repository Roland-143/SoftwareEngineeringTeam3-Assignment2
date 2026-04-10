type EmptyStateProps = {
  message: string;
};

function EmptyState({ message }: EmptyStateProps) {
  return (
    <section className="empty-state">
      <p>{message}</p>
    </section>
  );
}

export default EmptyState;