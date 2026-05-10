export default function Speedometer({ value, label }) {
  const radius = 90;
  const circumference = Math.PI * radius;
  const progress = Math.min(Math.max(value, 0), 100);
  const offset = circumference - (progress / 100) * circumference;

  const getColor = () => {
    if (progress >= 70) return "text-green-600 stroke-green-600";
    if (progress >= 40) return "text-yellow-500 stroke-yellow-500";
    return "text-red-500 stroke-red-500";
  };

  return (
    <div className="flex flex-col items-center">
      <svg width="220" height="120">
        {/* Background arc */}
        <path
          d="M20 100 A90 90 0 0 1 200 100"
          fill="none"
          stroke="#e5e7eb"
          strokeWidth="14"
        />

        {/* Progress arc */}
        <path
          d="M20 100 A90 90 0 0 1 200 100"
          fill="none"
          strokeWidth="14"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          className={getColor()}
          style={{ transition: "stroke-dashoffset 0.8s ease" }}
        />
      </svg>

      <div className="text-3xl font-bold -mt-6">{progress}%</div>
      <div className={`text-lg font-semibold ${getColor()}`}>{label}</div>
    </div>
  );
}
