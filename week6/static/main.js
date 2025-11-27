document.addEventListener('DOMContentLoaded', () => {
  // confirm deleting action
  const deleteForms = document.querySelectorAll(".delete-form");
  deleteForms.forEach(form => {
    form.onsubmit = function () { // 也可以用inline JavaScript：onsubmit="return confirm('確定要刪除嗎？');"
      return confirm("確定要刪除嗎？");
    };
  });
});

