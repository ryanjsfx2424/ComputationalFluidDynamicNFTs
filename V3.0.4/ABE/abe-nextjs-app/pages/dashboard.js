import Head from 'next/head'
import Image from 'next/image'
import styles from '../styles/Home.module.css'

export default function Home() {
  return (
    <div className={styles.container}>
      <Head>
        <title>ABE - Dashboard</title>
        <meta name="description" content="Always Be Early (ABE) by Ei Labs" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <h1 className={styles.title}>
          ABE Dashboard
        </h1>
      </main>
    </div>
  )
}
