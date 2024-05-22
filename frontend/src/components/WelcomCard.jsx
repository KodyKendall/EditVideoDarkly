import { Link } from 'react-router-dom';

function WelcomeCard() {
  return (
    <div className="max-w-sm mx-auto bg-gray-500 rounded-lg shadow-md overflow-hidden my-10">
      <div className="p-5">
        <h2 className="text-lg font-semibold text-white">Welcome to Pony Express!</h2>
        <p className="text-white mt-2">
            Pony Express is the world's first Web 3.0 messaging app. Made possible with blockchain, AI, Machine Learning, Cloud Computing, and [other trendy tech buzzwords]!
        </p>
        <div className="mt-4">
          <div className="mt-4 flex justify-center"> {/* Added flex and justify-center classes here */}
            <Link to="/login" className="inline-block bg-violet-500 text-white font-bold py-2 px-4 rounded hover:bg-violet-600">
              Get Started!
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

export default WelcomeCard;
