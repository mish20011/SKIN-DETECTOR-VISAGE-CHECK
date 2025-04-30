import React from 'react';
import GithubLogoLight from '../images/githubLight.png';
import LinkdinLogo from '../images/LinkedInDark.png';
import GithubLogoDark from '../images/githubDark.jpg';

function SocialMedia({ Theme }) {
  const RenderGithubLogo = () => {
    return Theme === 'Light' ? (
      <img src={GithubLogoLight} alt="Github Logo Light" className="github-logo" />
    ) : (
      <img src={GithubLogoDark} alt="Github Logo Dark" className="github-logo-dark" />
    );
  };

  return (
    <div className="icons">

      {/* GitHub Icon */}
      <a
        href="https://github.com/TheUnmeshRaj/SkinDiseaseAI2"
        target="_blank"
        rel="noopener noreferrer"
        className={`github-icon github-${Theme}`}
      >
        <RenderGithubLogo />
      </a>
    </div>
  );
}

export default SocialMedia;