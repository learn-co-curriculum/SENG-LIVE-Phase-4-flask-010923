import React, { useState, useRef } from "react";
import { Link } from "react-router-dom";
import rocket from "../assets/pngwing.com.png";
import newFrontier from "../assets/8d82b5_Star_Trek_Theme_Song.mp3";

function Header() {
  const [isPlaying, setIsPlaying] = useState(false);

  const space = useRef(new Audio(newFrontier));

  const handleLogoClick = () => {
    if (!isPlaying) {
      space.current.play();
      space.current.loop = true;
    } else {
      space.current.pause();
    }
    setIsPlaying(!isPlaying);
  };
  return (
    <nav>
      <img onClick={handleLogoClick} src={rocket} alt="" />
      <span>
        <h1>
          <Link to="/">Cosmic Travel Agency</Link>
        </h1>
      </span>
    </nav>
  );
}

export default Header;
