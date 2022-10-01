import { useState, useEffect } from 'react';

import Head from 'next/head'
import Image from 'next/image'
import Link from 'next/link'

import Aos from "aos";
import "aos/dist/aos.css";

import styles from '../styles/Home.module.css'
import pokerChip from '../public/images/poker-chip.svg'
import Header from '../components/header'


export default function Home() {
	const [showInitialText,  setShowInitialText ] = useState(false)
	const [showInitialImage, setShowInitialImage] = useState(false)

	useEffect(() => {
		Aos.init({ duration: 1500 });
		setTimeout(function() {
			setShowInitialImage(true)
		}, 500)
		setTimeout(function() {
			setShowInitialText(true)
		}, 2000)
	}, []);


  return (
    <div className={styles.container}>
      <Head>
        <title>PokerLegens</title>
        <meta name="description" content="PokerLegens - web3 poker" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      {/* <Flex className={styles.intro}/> */}
      {/* Next up, do an intro animation like RDH does! */}

      <Header/>

      <main className={styles.main}>
        <h1 className={styles.title}>
          Welcome to PokerLegens
          <br></br>
          <Link href="/dapp">Enter the Dapp</Link>
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
