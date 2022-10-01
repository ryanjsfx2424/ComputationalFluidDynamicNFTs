import Head from 'next/head'
import Image from 'next/image'
import Link from 'next/link'
import styles from '../styles/Home.module.css'
import pokerChip from '../public/images/poker-chip.svg'
import Header from '../components/header'

export default function Dapp() {
  return (
    <div className={styles.container}>
      <Head>
        <title>PokerLegens</title>
        <meta name="description" content="PokerLegens - web3 poker" />
        <link rel="icon" href="/favicon.ico" />
      </Head>


      <main className={styles.main}>
        <h1 className={styles.title}>
          Welcome to PokerLegens
          <br></br>
          <Link href="/">Go Home</Link>
        </h1>
      </main>

      <footer className={styles.footer}>
        <a
          href="https://twitter.com/pokerlegens"
          target="_blank"
          rel="noopener noreferrer"
        >
          Powered by{' '}
          <span className={styles.logo}>
            <Image src={pokerChip} alt="PokerLegens Logo" width={72} height={16} />
          </span>
        </a>
      </footer>
    </div>
  )
}
