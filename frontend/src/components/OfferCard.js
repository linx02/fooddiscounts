const OfferCard = ({ offer }) => {
    return (
        <>
        <div className="relative offer-card inline-block w-36 h-36 shadow-md rounded-xl">
            <img src={offer.image} alt="product" className="w-full h-auto rounded-xl" />
            <div className="absolute bottom-0 right-0 bg-[#fdf250] p-2 rounded-xl">
                <p className="text-xs font-semibold text-[#d02d22]">Pris: {parseFloat(offer.price.toFixed(2))}kr</p>
                <p className="text-xs font-semibold text-[#d02d22]">Rabatt: {offer.savings != 0 ? parseFloat(offer.savings.toFixed(2)) + 'kr' : '?'}</p>
                <p className="text-xs text-neutral-600">Minsta köp: {offer.min_quantity}st</p>
            </div>
        </div>
        <p className="text-sm font-semibold pt-2">{offer.name}</p>
        </>
    );
}

export default OfferCard;