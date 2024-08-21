import React from 'react';
import { useState, useEffect } from 'react';
import { Swiper, SwiperSlide } from 'swiper/react';
import 'swiper/css';
import OfferCard from './OfferCard';

const StatisticsModal = ({ state, setState, statistics }) => {
    return (
        state &&
        <div className='fixed top-0 left-0 z-50 w-full h-full bg-black bg-opacity-50 flex items-center justify-center'>
            <div className='bg-white p-4 rounded-lg'>
                <p className='text-xl font-semibold'>Statistik</p>
                <p className='text-lg'>Median sparande kr: <span className='font-semibold'>{parseFloat(statistics.median_savings_kr.toFixed(2))}</span></p>
                <p className='text-lg'>Median sparande %: <span className='font-semibold'>{parseFloat(statistics.median_savings_percent.toFixed(2))}</span></p>
                <p className='text-lg'>Median pris kr: <span className='font-semibold'>{parseFloat(statistics.median_price.toFixed(2))}</span></p>
                <p className='text-lg'>Antal erbjudanden: <span className='font-semibold'>{parseFloat(statistics.total_offers.toFixed(2))}</span></p>
                <button className='bg-blue-500 text-white p-2 rounded-lg mt-4' onClick={() => setState(!state)}>Stäng</button>
            </div>
        </div>
    );
}

const OfferSlider = ({ offers, logo, sideText, statistics }) => {

    const [modalVisible, setModalVisible] = useState(false);

    return (
        <div>
            <div className='flex justify-between mr-4'>
                <div className='flex items-center'>
                    <img src={logo} alt="Store logo" className='h-10 m-4' />
                    {sideText && <p className='text-3xl text-red-500 font-semibold'>{sideText}</p>}
                </div>
                <button className='text-blue-600' onClick={() => setModalVisible(!modalVisible)}>
                    Se statistik
                </button>
            </div>
            <Swiper
                spaceBetween={30}
                slidesPerView={3}
                pagination={{ clickable: true }}
            >
                {offers.map((offer, index) => (
                    <SwiperSlide key={index}>
                        <OfferCard offer={offer} />
                    </SwiperSlide>
                ))}
            </Swiper>

            <StatisticsModal state={modalVisible} setState={setModalVisible} statistics={statistics} />
        </div>
    );
}

export default OfferSlider;