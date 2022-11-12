import PerfectScrollbar from 'react-perfect-scrollbar';
import { InfoCard } from './Info-card';
export const PengumumanList = ({ pengumumans, ...rest }) => {
    return (
        <PerfectScrollbar>
        
            {pengumumans.map((pengumuman) => <InfoCard key={pengumuman.id} info={pengumuman} />)}
        </PerfectScrollbar>
    );
}