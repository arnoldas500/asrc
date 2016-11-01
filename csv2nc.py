--Boundary-00=_K6HsJyi/OUlNDCX
Content-Type: text/plain; charset="iso-8859-1"; name="csv2nc.jnl"
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="csv2nc.jnl"

 ! Convert CSV file to NetCDF
 ! Requires one parameter, the name of a CSV file to convert.
 ! Each column of the file must have a name in the first row (trailing unnamed
 columns are dropped)
 ! The alphanumeric portion of the column names must be unique
 !
 ! author: gordon.keith@xxxxxxxx

let csv_cols={spawn:"head -1 $1 | sed s/[^a-z,A-Z_0-9]//g | sed 's/,*$//'"}
columns/var="`csv_cols`"/skip=1 $1
save/file=$1.nc/clobber `csv_cols`

 ! apply long names and units
use $1.nc
let csv_vars="`csv_cols`"
let csv_ttls={spawn:"head -1 $1 | sed 's/[\"\"]//g'"}
let csv_unit={spawn:"head -1 $1 | sed 's/[\"\"]//g' | sed 's/,[^,(]*(/,(/g' |
sed 's/)[^,]*,/),/g' | sed 's/,[^,(]*,/,,/g' | sed 's/,[^,(][^,(]*,/,,/g' | sed
's/^[^,(]*//' | sed 's/[),][^),]*$//' | sed 's/[)(]//g'"}
repeat/range=1:`strlen(csv_vars)` (  \
   let csv_vc=strindex(csv_vars,",") ;    \
   let csv_tc=strindex(csv_ttls,",") ;    \
   let csv_uc=strindex(csv_unit,",") ;    \
   if `csv_vc EQ 0` then exit/loop ;  \
   let csv_var=substring(csv_vars,1,csv_vc - 1) ;\
   if `csv_tc GT 1` then define att/output/type=string
   `csv_var`.long_name="`substring(csv_ttls,1,csv_tc - 1)`"  ; \
   if `csv_uc GT 1` then define att/output/type=string
   `csv_var`.units="`substring(csv_unit,1,csv_uc - 1)`" ; \
   let csv_vars=substring("`csv_vars`",`csv_vc` + 1, 20480) ; \
   let csv_ttls=substring("`csv_ttls`",`csv_tc` + 1, 20480) ; \
   let csv_unit=substring("`csv_unit`",`csv_uc` + 1, 20480) ; \
)
if `csv_tc GT 1` then
   define att/output/type=string
   `csv_vars`.long_name="`substring(csv_ttls,1,csv_tc - 1)`"
elif `strlen(csv_ttls) GT 0` then
   define att/output/type=string `csv_vars`.long_name="`csv_ttls`"
endif
if `csv_uc EQ 1` then
elif `csv_uc GT 1` then
   define att/output/type=string `csv_vars`.units="`substring(csv_unit,1,csv_uc
   - 1)`"
elif `strlen(csv_unit) GT 0` then
   define att/output/type=string `csv_vars`.units="`csv_unit`"
endif
save/file=$1.nc/clobber `csv_cols`


--Boundary-00=_K6HsJyi/OUlNDCX--
