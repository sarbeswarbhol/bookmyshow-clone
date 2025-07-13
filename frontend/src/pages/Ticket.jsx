import { useLocation, useNavigate } from "react-router-dom";
import { useEffect } from "react";

function Ticket() {
  const location = useLocation();
  const navigate = useNavigate();

  // Simulate receiving ticket data from previous page
  const ticket = location.state?.ticket;

  useEffect(() => {
    if (!ticket) {
      navigate("/");
    }
  }, [ticket, navigate]);

  if (!ticket) return null;

  return (
    <div className="min-h-screen bg-light p-6 flex justify-center">
      <div className="bg-white shadow-md rounded-lg p-6 max-w-md w-full text-center">
        <h2 className="text-2xl font-bold text-dark mb-4">🎟️ Ticket Confirmed!</h2>
        <p className="text-muted mb-2">Movie: <span className="text-dark font-medium">{ticket.movie}</span></p>
        <p className="text-muted mb-2">Theater: <span className="text-dark font-medium">{ticket.theater}</span></p>
        <p className="text-muted mb-2">Date: <span className="text-dark font-medium">{ticket.date}</span></p>
        <p className="text-muted mb-2">Time: <span className="text-dark font-medium">{ticket.time}</span></p>
        <p className="text-muted mb-2">Seats: <span className="text-dark font-medium">{ticket.seats.join(", ")}</span></p>
        <p className="text-muted mb-4">Amount Paid: ₹<span className="text-dark font-medium">{ticket.amount}</span></p>

        <button
          onClick={() => navigate("/")}
          className="bg-primary text-white px-6 py-2 rounded hover:bg-red-600"
        >
          Go to Home
        </button>
      </div>
    </div>
  );
}

export default Ticket;
