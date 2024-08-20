import React from 'react';
import { Swiper, SwiperSlide } from 'swiper/react';
import 'swiper/css';
import OfferCard from './OfferCard';

const OfferSlider = ({ offers, logo, sideText }) => {
    return (
        <div>
            <div className='flex items-center'>
                <img src={logo} alt="Store logo" className='h-10 m-4' />
                {sideText && <p className='text-3xl text-red-500 font-semibold'>{sideText}</p>}
            </div>
            <Swiper
                spaceBetween={70}
                slidesPerView={3}
                pagination={{ clickable: true }}
                navigation={true}
            >
                {offers.map((offer, index) => (
                    <SwiperSlide key={index}>
                        <OfferCard offer={offer} />
                    </SwiperSlide>
                ))}
            </Swiper>
        </div>
    );
}

export default OfferSlider;