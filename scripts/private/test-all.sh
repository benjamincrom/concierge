ROOT_DIR=`dirname $0`/../..
SANDBOX_DIR=$ROOT_DIR/angular-phonecat-snapshots/sandbox
cd $SANDBOX_DIR

for i in {0..12}
do
  ./goto_step.sh $i
  karma start config/karma.conf.js --browsers --single-run
  karma start config/karma-e2e.conf.js --browsers --single-run
done