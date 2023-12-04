import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './navbar.css';

const Navbar = () => {
    const [selectedTab, setSelectedTab] = useState('home');
    let navigate = useNavigate()

    const handleTabClick = (tab) => {
        setSelectedTab(tab);
        navigate("/"+tab)
    };

    return (
        <div className="navbar">
        <div
            className={`tab ${selectedTab === 'home' ? 'selected' : ''}`}
            onClick={() => handleTabClick('home')}
        >
            Home
        </div>
        <div
            className={`tab ${selectedTab === 'instructions' ? 'selected' : ''}`}
            onClick={() => handleTabClick('instructions')}
        >
            Instructions
        </div>
        <div
            className={`tab ${selectedTab === 'play' ? 'selected' : ''}`}
            onClick={() => handleTabClick('play')}
        >
            Play
        </div>
        <div className="underline" style={{ left: selectedTab === 'home' ? '10px' : selectedTab === 'instructions' ? 'calc(50% - 50px)' : 'calc(100% - 110px)' }}></div>
        </div>
    );
};

export default Navbar;