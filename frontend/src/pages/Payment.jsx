import { useLocation, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";

const tabs = ["Wallet", "UPI", "Card", "NetBanking"];

function Payment() {
  const navigate = useNavigate();
  const location = useLocation();
  const booking = location.state?.booking;

  const [activeTab, setActiveTab] = useState("Wallet");
  const [formData, setFormData] = useState({});
  const [card, setCard] = useState("");
  const [upi, setUpi] = useState("");
  const [bank, setBank] = useState("");

  useEffect(() => {
    if (!booking) navigate("/");
  }, [booking]);

  const totalAmount = booking?.seats.length * 200;

  const handlePay = () => {
    navigate("/ticket", {
      state: {
        ticket: {
          ...booking,
          amount: totalAmount,
        },
      },
    });
  };

  const isDisabled = () => {
    if (activeTab === "Wallet") return false; // Always available
    if (activeTab === "UPI" && upi.trim().length === 0) return true;
    if (activeTab === "Card" && card.trim().length < 16) return true;
    if (activeTab === "NetBanking" && !bank) return true;
    return false;
  };

  if (!booking) return null;

  return (
    <div className="min-h-screen bg-light p-6 flex justify-center">
      <div className="bg-white shadow-md rounded-lg w-full max-w-lg p-6">
        <h2 className="text-2xl font-bold text-dark mb-4">Pay ₹{totalAmount}</h2>

        {/* Tabs */}
        <div className="flex mb-6 border-b">
          {tabs.map(tab => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-4 py-2 font-medium ${
                activeTab === tab
                  ? "border-b-4 border-primary text-dark"
                  : "text-muted"
              }`}
            >
              {tab}
            </button>
          ))}
        </div>

        {/* Wallet */}
        {activeTab === "Wallet" && (
          <div className="text-center space-y-4">
            <p className="text-muted">Using Paytm Wallet Balance</p>
            <p className="text-dark font-semibold">Available Balance: ₹999</p>
          </div>
        )}

        {/* UPI */}
        {activeTab === "UPI" && (
          <div>
            <label className="block mb-1 text-muted">Enter UPI ID</label>
            <input
              type="text"
              placeholder="example@upi"
              value={upi}
              onChange={(e) => setUpi(e.target.value)}
              className="w-full border border-muted p-2 rounded focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>
        )}

        {/* Card */}
        {activeTab === "Card" && (
          <div className="space-y-4">
            <input
              type="text"
              placeholder="Card Number"
              value={card}
              onChange={(e) => setCard(e.target.value)}
              className="w-full border border-muted p-2 rounded"
            />
            <div className="flex gap-2">
              <input
                type="text"
                placeholder="MM/YY"
                className="w-1/2 border border-muted p-2 rounded"
              />
              <input
                type="text"
                placeholder="CVV"
                className="w-1/2 border border-muted p-2 rounded"
              />
            </div>
          </div>
        )}

        {/* NetBanking */}
        {activeTab === "NetBanking" && (
          <div>
            <label className="block mb-1 text-muted">Select Bank</label>
            <select
              value={bank}
              onChange={(e) => setBank(e.target.value)}
              className="w-full border border-muted p-2 rounded"
            >
              <option value="">-- Select --</option>
              <option value="HDFC">HDFC Bank</option>
              <option value="ICICI">ICICI Bank</option>
              <option value="SBI">State Bank of India</option>
              <option value="AXIS">Axis Bank</option>
            </select>
          </div>
        )}

        <button
          onClick={handlePay}
          disabled={isDisabled()}
          className={`mt-6 w-full py-3 text-white font-bold rounded ${
            isDisabled() ? "bg-muted cursor-not-allowed" : "bg-primary hover:bg-red-600"
          }`}
        >
          Pay Now
        </button>
      </div>
    </div>
  );
}

export default Payment;
