import { loadStripe } from "@stripe/stripe-js";
import { motion } from "framer-motion";
import { bareAPI } from "../api/";
import { CheckCircle } from "react-feather"
type Props = {
  plan: string;
  price: string;
  id: string;
  metadata?: any;
  isPopular: boolean;
  monthly: boolean;
};

const Card = ({ plan, price, id, metadata, isPopular, monthly }: Props) => {
  const items = []
  for (const [key, value] of Object.entries(metadata)) {
    items.push(
      <p key={key + value} className="flex items-center text-gray-600 mb-2">
        <span className="w-4 h-4 mr-2 inline-flex items-center justify-center bg-gray-400 text-white rounded-full flex-shrink-0">
          <CheckCircle />
        </span>
        {key}: {value}
      </p>
    )
  }
  const handleCheckout = async () => {
    const stripe = await loadStripe(
      "pk_test_518h2jFItAhzYJ7dgwgnoYIDrufudKMsxdhAaa2YZt0YcbM5z1EfBvxYprkufs4KJO76zTkfaXSS3OSBtn6GMDmMm00C1wwlqJb"
    );
    const config = {
      headers: {
        "Content-Type": "application/json",
      },
    };
    const body = {
      priceId: id,
    };
    bareAPI
      .post("/api/v1/create-checkout-session/", body, config)
      .then((res) => {
        stripe?.redirectToCheckout({ sessionId: res.data.sessionId });
      })
      .catch((err) => { });
  };
  return (
    <div className="p-4 xl:w-1/4 md:w-1/2 w-full">
      <div
        className={`h-full p-6 rounded-lg border-2 border-${isPopular ? "indigo" : "gray"
          }-500 flex flex-col relative overflow-hidden`}
      >
        {isPopular ? (
          <span className="bg-indigo-500 text-white px-3 py-1 tracking-widest text-xs absolute right-0 top-0 rounded-bl">
            POPULAR
          </span>
        ) : (
          ""
        )}
        <h2 className="text-sm tracking-widest title-font mb-1 font-medium">
          {plan}
        </h2>
        <motion.h1 initial={{ x: -1000 }} animate={{ x: 0 }} className="text-5xl text-gray-900 leading-none flex items-center pb-4 mb-4 border-b border-gray-200">
          <span>${price}</span>
          <span className="text-lg ml-1 font-normal text-gray-500">{monthly ? '/mo' : '/yr'}</span>
        </motion.h1>
        {items}
        <button
          onClick={handleCheckout}
          className={`flex items-center mt-auto text-white bg-${isPopular ? 'indigo-700' : 'indigo-500'} border-0 py-2 px-4 w-full focus:outline-none hover:bg-indigo-600 rounded`}
        >
          Subscribe
          <svg
            fill="none"
            stroke="currentColor"
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            className="w-4 h-4 ml-auto"
            viewBox="0 0 24 24"
          >
            <path d="M5 12h14M12 5l7 7-7 7" />
          </svg>
        </button>
        <p className="text-xs text-gray-500 mt-3">You can cancel anytime.</p>
      </div>
    </div>
  );
};

export default Card;
