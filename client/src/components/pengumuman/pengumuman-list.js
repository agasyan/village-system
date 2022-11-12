import PerfectScrollbar from 'react-perfect-scrollbar';
import { InfoCard } from './Info-card';
export const PengumumanList = ({ pengumumans, ...rest }) => {
    return (
        <PerfectScrollBar>
            {pengumumans.map((pengumuman) => <InfoCard info={pengumuman} />)}
        </PerfectScrollBar>
    );
}