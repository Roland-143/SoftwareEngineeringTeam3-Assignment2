type SummaryCardsProps = {
  totalStudents: number;
  averageScore: string;
};

function SummaryCards({ totalStudents, averageScore }: SummaryCardsProps) {
  return (
    <section className="summary-section">
      <div className="summary-card">
        <h2>Total Students</h2>
        <p>{totalStudents}</p>
      </div>

      <div className="summary-card">
        <h2>Average Score</h2>
        <p>{averageScore}</p>
      </div>
    </section>
  );
}

export default SummaryCards;