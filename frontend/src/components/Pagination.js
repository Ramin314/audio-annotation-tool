import React from 'react';

const Pagination = ({ currentPage, hasMore, setCurrentPage }) => {
  const handlePrevious = () => {
    if (currentPage > 1) setCurrentPage(currentPage - 1);
  };

  const handleNext = () => {
    if (hasMore) setCurrentPage(currentPage + 1);
  };

  return (
    <div className='ui container center aligned' style={{ marginTop: '20px' }}>
      <button
        className='ui button'
        onClick={handlePrevious}
        disabled={currentPage === 1}
      >
        Previous
      </button>
      <button
        className='ui button'
        onClick={handleNext}
        disabled={!hasMore}
      >
        Next
      </button>
    </div>
  );
};

export default Pagination;
