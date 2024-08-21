import OfferSlider from "./components/OfferSlider";
import { useState, useEffect } from "react";

function App() {

  const [data, setData] = useState(null);

  useEffect(() => {
    // fetch("http://207.127.89.107:5000/api", { mode: "cors" })
    fetch("http://localhost:5000/api", { mode: "cors" })
      .then((response) => response.json())
      .then((data) => setData(data));
  }, []);

  return (
    <main>
      {data ?
      <div className="flex flex-col space-y-8 my-6">
        <OfferSlider offers={data.willys.offers} statistics={data.willys.statistics} logo="/images/willys.png" />
        <OfferSlider offers={data.lidl.offers} statistics={data.lidl.statistics} logo="/images/lidl.png" />
        <OfferSlider offers={data.ica_fjallbacken.offers} statistics={data.ica_fjallbacken.statistics} logo="/images/ica.png" sideText="Fjällbacken" />
        <OfferSlider offers={data.ica_maxi.offers} statistics={data.ica_maxi.statistics} logo="/images/ica.png" sideText="Maxi" />
        <OfferSlider offers={data.ica_soder.offers} statistics={data.ica_soder.statistics} logo="/images/ica.png" sideText="Söder" />
      </div>
      :
      <p className="text-xl text-center">Laddar...</p>
      }
    </main>
  );
}

export default App;
