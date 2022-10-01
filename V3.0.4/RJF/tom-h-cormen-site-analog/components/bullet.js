import Image from 'next/image'
import yellowSq from '../public/yellowsq.gif'

export default function Bullet() {
    return (
        <Image
            src={yellowSq}
            alt="yellow square bullet point"
            width={9}
            height={9}
            align="middle"
        >
        </Image>
)}