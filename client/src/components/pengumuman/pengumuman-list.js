import { CircularProgress } from '@mui/material';
import axios from 'axios';
import { useEffect, useState } from 'react';
import PerfectScrollbar from 'react-perfect-scrollbar';
import { InfoCard } from './Info-card';
export const PengumumanList = ({ ...rest }) => {
    const [pengumumans, setPengumumans] = useState([]);
    const [loading, setLoading] = useState(true);
    const fetchData = () => {
        axios
            .get('https://desa.agasyan.my.id/api/pengumuman/all')
            .then((response) => {
                const { data } = response;
                setLoading(false)
                 if (response.status === 200) {
                    //check the api call is success by stats code 200,201 ...etc
                    setPengumumans(data.sort((a, b) => (a.created_at_utc < b.created_at_utc) ? 1 : -1))
                } else {
                    //error handle section
                }
            })
            .catch((error) => console.log(error));
    };
    useEffect(() => {
        fetchData();
    }, []);
    return (
        <PerfectScrollbar>
            {loading && <CircularProgress />}
            {pengumumans.map((pengumuman) => <InfoCard key={pengumuman.id} info={pengumuman} />)}
        </PerfectScrollbar>
    );
}