import { useNavigate } from 'react-router-dom';

const ComparisonLayout = () => {
  const navigate = useNavigate();

  const handleSubmit = () => {
    // Do validation or saving here (later if needed)
    navigate('/next');
  };

  return (
    <div className="bg-white p-6 rounded-2xl shadow-md w-[90%] mx-auto">
      <div className="text-xl font-semibold mb-4">Enter Title</div>

      {/* ... buttons, sections, etc ... */}

      <div className="flex justify-center mt-8">
        <Button
          className="bg-gray-700 hover:bg-gray-800 text-white px-6 py-2 rounded-md"
          onClick={handleSubmit}
        >
          Submit
        </Button>
      </div>
    </div>
  );
};

export default ComparisonLayout;
