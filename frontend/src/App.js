import OfferSlider from "./components/OfferSlider";
import { useState, useEffect } from "react";

function App() {

  const [data, setData] = useState(null);

  useEffect(() => {
    fetch("http://localhost:5000/api", { mode: "cors" })
      .then((response) => response.json())
      .then((data) => setData(data));
  }, []);

  console.log(data);

  return (
    <main>
      {data ?
      <div className="flex flex-col space-y-8 my-6">
        <OfferSlider offers={data.willys.offers} logo="/images/willys.png" />
        <OfferSlider offers={data.ica_fjallbacken.offers} logo="/images/ica.png" sideText="Fjällbacken" />
        <OfferSlider offers={data.ica_maxi.offers} logo="/images/ica.png" sideText="Maxi" />
        <OfferSlider offers={data.ica_soder.offers} logo="/images/ica.png" sideText="Söder" />
      </div>
      :
      <p className="text-xl text-center">Laddar...</p>
      }
    </main>
  );
}

export default App;
