import Head from 'next/head'
import styles from '../styles/Home.module.css'

function AvgCase({ avgCase }) {
  if (avgCase > 25) {
    const caseRisk = 'Red'
    return <p style={{color: 'red'}}>{'Avg Cases per 100k - ' + avgCase}</p>
  } else if (avgCase >= 10 && avgCase < 25) {
    const caseRisk = 'Orange'
    return <p style={{color: 'orange'}}>{'Avg Cases per 100k - ' + avgCase}</p>
  } else if (avgCase >= 1 && avgCase < 10) {
    const caseRisk = 'Yellow'
    return <p style={{color: '#f5da2f'}}>{'Avg Cases per 100k - ' + avgCase}</p>
  } else {
    const caseRisk = 'Green'
    return <p style={{color: 'green'}}>{'Avg Cases per 100k - ' + avgCase}</p>
  }
}

function PosRate({ testData }) {
  if (testData > 25) {
    const caseRisk = 'Red'
    return <p style={{color: 'red'}}>{'Test Positivity Rate - ' + testData + '%'}</p>
  } else if (testData >= 10 && testData < 25) {
    const caseRisk = 'Orange'
    return <p style={{color: 'orange'}}>{'Test Positivity Rate - ' + testData + '%'}</p>
  } else if (testData >= 1 && testData < 10) {
    const caseRisk = 'Yellow'
    return <p style={{color: '#f5da2f'}}>{'Test Positivity Rate - ' + testData + '%'}</p>
  } else if (testData == 'Not Avalilable') {
    return <p>{'Test Positivity Rate - NA'}</p>
  } else {
    const caseRisk = 'Green'
    return <p style={{color: 'green'}}>{'Test Positivity Rate - ' + testData + '%'}</p>
  }
}

export default function Home({ jsonData }) {

  return (
    <div className={styles.container}>
      <Head>
        <meta name="google-site-verification" content="yoEsDzF13VOK_wtcU06db6JXzs9bPmJa7EQJxO-kv2o" />
        <title>Covid Vaccine and Risk Dashboard</title>
        <meta name="description" content="Vaccine and Covid risk tracker for India" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <h1 className={styles.title}>
          Covid Dashboard
        </h1>

        <p className={styles.description}>
          Dashboard for tracking covid risk levels and vaccination
        </p>

        <div className={styles.grid}>
          {jsonData.map((data) =>
            <div className={styles.card}>
              <h2>{data['Place']}</h2>
              <AvgCase avgCase={data['Avg Cases']}/>
              <PosRate testData={data['Avg Positivity Rate']}/>
              <p>{'Approx. time for 75% vaccination - ' + data['Days'] + ' days'}</p>
            </div>
          )}
        </div>
      </main>
    </div>
  )
}

export async function getStaticProps() {
  const res = await fetch(
    'https://raw.githubusercontent.com/Pranavb333/covid-dashboard-data/main/data.json',
    {
      method: "GET"
    }
  )
  const jsonData = await res.json()

  return {
    props: {
      jsonData,
    },
  }
}
