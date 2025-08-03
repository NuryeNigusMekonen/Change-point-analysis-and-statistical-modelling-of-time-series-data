useEffect(() => {
  fetch("/api/data")
    .then((res) => res.json())
    .then((data) => {
      console.log("Received from backend:", data);
    });
}, []);
