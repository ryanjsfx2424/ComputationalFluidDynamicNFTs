import styles from '../styles/Home.module.css'
import Image from 'next/image'
import pokerChip from '../public/images/poker-chip.svg'

export default function Header() {
    return (

        <header className={styles.header}>
            <Image src={pokerChip} alt="poker chip logo"/>
            PokerLegens
        </header>
)}